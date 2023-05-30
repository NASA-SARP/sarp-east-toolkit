from platform import system

import sarp_east_toolkit


def test_netrc(tmpdir, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'testuser')
    monkeypatch.setattr('getpass.getpass', lambda _: 'testpass')
    sarp_east_toolkit.earthdata_login(tmpdir)
    netrc = '_netrc' if system()=='Winows' else '.netrc'
    assert (tmpdir / netrc).exists()


def test_s3(monkeypatch):
    monkeypatch.setenv('AWS_REGION', 'test_region')
    fs = sarp_east_toolkit.earthdata_s3fs('gesdisc')
    assert fs.secret
