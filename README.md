# SARP East Toolkit

A tiny, poorly documented package to speed student setup.

## Installation

```
pip install --user git+https://github.com/NASA-SARP/sarp-east-toolkit.git
```

## Usage

The `earthdata_s3fs` function returns an appropriately credentialled S3 File System object
for opening science data files from the given DAAC with XArray's default NetCDF engine. If a
suitable "netrc" file is not found, the `earthdata_login` method will create one after
requesting your username and password.

```
import xarray
from sarp_east_toolkit import earthdata_s3fs

fs = earthdata_s3fs('gesdisc')
fileobj = (
    's3://gesdisc-cumulus-prod-protected/'
    'OCO3_DATA/OCO3_L2_Lite_FP.10.4r/2020/'
    'oco3_LtCO2_200228_B10400Br_220317235859s.nc4'
)
dataset = xarray.open_dataset(fs.open(fileobj), chunks={})
dataset
```

The `earthdata_rio` function returns an appropriately credentialled `rasterio.Env` object
for opening geospatial raster files with XArray's rasterio engine.

```
import xarray
from sarp_east_toolkit import earthdata_rio

rio_env = earthdata_rio('ornldaac')
fileobj = (
    's3://ornl-cumulus-prod-protected/'
    'gedi/GEDI_L4B_Gridded_Biomass/data/'
    'GEDI04_B_MW019MW138_02_002_05_R01000M_MU.tif'
)
with rio_env as env:
    raster = xarray.open_dataset(fileobj, engine='rasterio', chunks={})
raster
```
