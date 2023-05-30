from netrc import netrc
from pathlib import Path
from platform import system
import getpass
import os

import requests
import s3fs


def earthdata_login(directory: Path|str|None = None) -> None:

    # Use home directory by default
    if not directory:
        directory = Path.home()
    else:
        directory = Path(directory)

    # Earthdata URL endpoint for authentication
    urs = 'urs.earthdata.nasa.gov'

    # Determine the OS specific name and full path for the netrc file
    # (Windows machines usually use an '_netrc' file)
    netrc_name = '_netrc' if system()=='Windows' else '.netrc'
    netrc_path = directory / netrc_name

    # Check, create, or append to the netrc file
    try:
        # determine if netrc file exists and includes this urs
        netrc(netrc_path).authenticators(urs)[0]
        return
    except FileNotFoundError:
        # set mode to create a new file
        mode = 'w'
    except TypeError:
        # set mode to append to an existing file
        mode = 'a'

    print('Enter your NASA Earthdata Login credentials.')
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    credential = f'machine {urs} login {username} password {password}\n'
    with open(netrc_path, mode) as stream:
        stream.write(credential)
    if mode == 'w':
        os.chmod(netrc_path, 0o600)


def earthdata_s3fs(daac: str) -> s3fs.S3FileSystem:

    # ensure netrc
    earthdata_login()

    # S3 credential providers
    endpoint = {
        'podaac': 'https://archive.podaac.earthdata.nasa.gov/s3credentials',
        'gesdisc': 'https://data.gesdisc.earthdata.nasa.gov/s3credentials',
        'lpdaac': 'https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials',
        'ornldaac': 'https://data.ornldaac.earthdata.nasa.gov/s3credentials',
        'ghrc': 'https://data.ghrc.earthdata.nasa.gov/s3credentials',
        'nsidc': 'https://data.nsidc.earthdatacloud.nasa.gov/s3credentials'
    }

    # get temporary credentials
    response = requests.get(endpoint[daac])
    credentials = response.json()

    # return credentialled file system
    return s3fs.S3FileSystem(
        key=credentials['accessKeyId'],
        secret=credentials['secretAccessKey'],
        token=credentials['sessionToken'],
        client_kwargs={'region_name': os.environ['AWS_REGION']},
    )
