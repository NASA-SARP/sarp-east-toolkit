# SARP East Toolkit

A tiny, poorly documented package to speed student setup.

## Installation

```
pip install git+https://github.com/NASA-SARP/sarp-east-toolkit.git
```

## Usage

The `earthdata_s3fs` function returns an appropriately credentialled S3 File System object
for streaming from the given DAAC. If a suitable "netrc" file is not found, the `earthdata_login`
method will create one after requesting your username and password.

```
from sarp_east_toolkit import earthdata_s3fs

fs = earthdata_s3fs('podaac')
```
