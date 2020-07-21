
def test_version():
    from apitest import __version__
    assert isinstance(__version__,str)