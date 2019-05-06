# Identifier remapping for gene and protein identifiers

This is a python script that can remap protein/gene identifiers into different formats. It relies on UniProt's identifier mapping service (see https://www.uniprot.org/help/api_idmapping and https://www.uniprot.org/help/uploadlists).

The script automatically splits big queries into smaller chunks and tries to retrieve the results multiple times upon failure.

## Usage

```
usage: id-remapping.py [-h] -i INPUT -f FROM_ID -t TO_ID -o OUTPUT -e EMAIL
                       [-m FORMAT] [-c CHUNK_SIZE] [-s SLEEP] [-r RETRIES]

Script to create identifier mapping files from various types of ids to uniprot
accession numbers.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File listing all identifiers that need to be remapped
                        to uniprot ACs. (default: None)
  -f FROM_ID, --from-id FROM_ID
                        Type of source identifier id. The database
                        abbreviations used by UniProt's mapping service, as
                        described here:
                        http://www.uniprot.org/help/api_idmapping (default:
                        None)
  -t TO_ID, --to-id TO_ID
                        Type of destination identifier id. The database
                        abbreviations used by UniProt's mapping service, as
                        described here:
                        http://www.uniprot.org/help/api_idmapping (default:
                        None)
  -o OUTPUT, --output OUTPUT
                        Location where output will be saved. (default: None)
  -e EMAIL, --email EMAIL
                        The e-mail address supplied to the API (see
                        https://www.uniprot.org/help/privacy). (default: None)
  -m FORMAT, --output-format FORMAT
                        The output format to request (default=tab). (default:
                        tab)
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        The output format to request (default=1000). (default:
                        1000)
  -s SLEEP, --sleep SLEEP
                        Wait time (seconds) in between chunks and retries
                        (default=5). (default: 5)
  -r RETRIES, --retries RETRIES
                        The number of retries to attempt upon encountering an
                        error (default=10). (default: 10)
```

## Example

Given an input file with UniProt accession numbers...

```
P08238
P10275
E9PAV3
O00170
O43504
```

...that should be remapped to RefSeq Protein identifiers (P_REFSEQ_AC as given by https://www.uniprot.org/help/api_idmapping), the following command can be used:

    id-remapping.py -i input.txt -f ACC -t P_REFSEQ_AC -o remapped_identifiers.tsv -e email@organization.com

This results in the following tab-delimited (by default) output file:

```
From    To
E9PAV3  XP_011536691.1
O00170  NP_001289888.1
O00170  NP_001289889.1
O00170  NP_003968.3
O43504  NP_006393.2
P08238  NP_001258898.1
P08238  NP_001258899.1
P08238  NP_001258900.1
P08238  NP_031381.2
P10275  NP_000035.2
P10275  NP_001011645.1
P10275  NP_001334990.1
P10275  NP_001334992.1
P10275  NP_001334993.1
```

## Dependencies

* numpy https://www.numpy.org/ (installable via `pip` or `conda`)