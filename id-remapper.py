import argparse
import time

import numpy as np
import requests

from pathlib import Path


def id_remap(
    array, from_id, to_id, savepath, email, format="tab", chunk_size=1000, sleep=5, retries=10
):
    """
    Create identifier mapping files between uniprot ACs and other types of identifiers.

    See:
        http://www.uniprot.org/help/api_idmapping
        https://www.uniprot.org/help/api_queries
        https://docs.python.org/3/howto/urllib2.html
        https://www.biostars.org/p/66904/
        https://www.biostars.org/p/163745/

    Parameters
    ----------
    array : array-like
        List of all identifiers that need to be remapped to
        UniProt Accession Numbers. E.g. [refseq:NP_001179, uniprotkb:Q16611, ...]
    from_id : string
        The source database abbreviation used by UniProt's mapping service, as
        described here: http://www.uniprot.org/help/api_idmapping
    to_id : string
        The destination database abbreviations used by UniProt's mapping service, as
        described here: http://www.uniprot.org/help/api_idmapping
    savepath : string
        Filepath where to write the mapping file.
    email : string
        The email address to provide to the uniprot API.
    format : str
        The output format to request.
        (Default='tab')
    chunk_size : int
        Size of the chunks that are submitted to the EBI mapping web service.
        (Default=1000)
    sleep : int
        Wait time (seconds) in between chunks and retries.
        (Default = 5 seconds)
    retries : int
        The number of retries to attempt upon encountering an error.
        (Default = 10)

    Returns
    -------
    None
        Writes mapping files to savepath.
    """

    # create output file
    savepath = Path(savepath)
    savepath.parent.mkdir(parents=True, exist_ok=True)

    # split request into 1000 sized chunks
    mapping_list = []
    progress_counter = 0

    for i in [array[j : j + chunk_size] for j in range(0, len(array), chunk_size)]:

        # cast object-typed array to space separated string
        ids_str = " ".join(np.char.mod("%s", i))

        url = "https://www.uniprot.org/uploadlists/"

        params = {"from": from_id, "to": to_id, "format": "tab", "query": ids_str}

        contact = email
        headers = {"User-Agent": f"Python {contact}"}

        request_completed = False
        n_tries = 0
        while not request_completed:
            if n_tries > retries:
                print(
                    "WARNING: Not all entries were downloaded. Please try again later."
                )
                mapping = None
                break
            n_tries += 1
            try:
                response = requests.get(url, params=params, headers=headers)
                mapping = response.text
                request_completed = True
            except requests.exceptions.RequestException as error:
                print(f"Encountered connection error, retrying (attempt {n_tries}).")
                print(error)
                time.sleep(sleep)
                pass
            except requests.exceptions.HTTPError as err:
                print(
                    f"HTTP error encountered, check network connection and query content, retrying (attempt {n_tries})."
                )
                print(err)
                time.sleep(sleep)
                pass

        mapping_list.append(mapping)
        progress_counter += chunk_size
        print("Queried first {} identifiers...".format(progress_counter))
        time.sleep(sleep)

    savepath.write_text("".join(mapping_list))

    print(
        "Created mapping file between UniProt ACs and {} in: {}.\n".format(
            from_id, savepath.resolve()
        )
    )


def read_array(input_file):
    with Path(input_file).open('r') as f:
        array = [line.strip() for line in f]
    # remove redundant entries
    array = np.unique(array)
    print("Retrieving mapping for {} unique ids".format(len(array)))
    return array


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to create identifier mapping files from various types of ids to uniprot accession numbers.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        required=True,
        help="File listing all identifiers that need to be remapped to uniprot ACs.",
    )
    parser.add_argument(
        "-f",
        "--from-id",
        dest="from_id",
        type=str,
        required=True,
        help="Type of source identifier id. The database abbreviations used by UniProt's mapping service, as described here: http://www.uniprot.org/help/api_idmapping",
    )
    parser.add_argument(
        "-t",
        "--to-id",
        dest="to_id",
        type=str,
        required=True,
        help="Type of destination identifier id. The database abbreviations used by UniProt's mapping service, as described here: http://www.uniprot.org/help/api_idmapping",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        required=True,
        help="Location where output will be saved.",
    )
    parser.add_argument(
        "-e",
        "--email",
        dest="email",
        type=str,
        required=True,
        help="The e-mail address supplied to the API (see https://www.uniprot.org/help/privacy).",
    )
    parser.add_argument(
        "-m",
        "--output-format",
        dest="format",
        type=str,
        required=False,
        default="tab",
        help="The output format to request (default=tab).",
    )
    parser.add_argument(
        "-c",
        "--chunk-size",
        dest="chunk_size",
        type=str,
        required=False,
        default=1000,
        help="The output format to request (default=1000).",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        dest="sleep",
        type=str,
        required=False,
        default=5,
        help="Wait time (seconds) in between chunks and retries (default=5).",
    )
    parser.add_argument(
        "-r",
        "--retries",
        dest="retries",
        type=str,
        required=False,
        default=10,
        help="The number of retries to attempt upon encountering an error (default=10).",
    )
    args = parser.parse_args()

    array = read_array(args.input)

    id_remap(
        array=array,
        from_id=args.from_id,
        to_id=args.to_id,
        savepath=args.output,
        email=args.email,
        format=args.format,
        chunk_size=args.chunk_size,
        sleep=args.sleep,
        retries=args.retries,
    )
