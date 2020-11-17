# drc-magic
# Function:

This script runs a magic drc check on a given GDSII.

# Prerequisites:

- Docker

# Setup:

To setup the necessary docker file, run:
```bash
    sh build-docker.sh
```

Or pull the docker:
```
docker pull ...
```
# How to use:

Mount the docker:

```
export PDK_ROOT=<the location where the pdk resides>
export TARGET_DIR=<the location where the target design residees>
docker run -it -v $TARGET_DIR:$TARGET_DIR \
    -v $PDK_ROOT:$PDK_ROOT \
    -e TARGET_DIR=$TARGET_DIR \
    -e PDK_ROOT=$PDK_ROOT \
    -u $(id -u $USER):$(id -g $USER) \
    efabless/drc_magic:latest
```

The following explains how to run the script:

```
usage: gds_drc_checker.py [-h] --design_name DESIGN_NAME [--pdk PDK]
                          [--target_type TARGET_TYPE]
                          [--output_directory OUTPUT_DIRECTORY]

Runs a magic drc check on a given GDSII.

optional arguments:
  -h, --help            show this help message and exit
  --design_name DESIGN_NAME, -d DESIGN_NAME
                        Design Name
  --pdk PDK, -p PDK     PDK used. Default = sky130A
  --target_type TARGET_TYPE, -tt TARGET_TYPE
                        Target type: gds, mag, def. Default = gds
  --output_directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                        Output Directory. Default = $TARGET_DIR/drc_checks
```
