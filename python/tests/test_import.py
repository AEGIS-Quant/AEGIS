def test_import_and_hello():
    import aegis
    assert hasattr(aegis, "hello")
    assert "hello" in str(aegis.hello()).lower()

