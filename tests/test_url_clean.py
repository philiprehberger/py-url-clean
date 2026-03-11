from philiprehberger_url_clean import clean, remove_params, normalize, clean_many


def test_clean_utm_params():
    url = "https://example.com/page?utm_source=twitter&utm_medium=social&id=123"
    result = clean(url)
    assert "utm_source" not in result
    assert "utm_medium" not in result
    assert "id=123" in result


def test_clean_fbclid():
    url = "https://example.com?fbclid=abc123&q=test"
    result = clean(url)
    assert "fbclid" not in result
    assert "q=test" in result


def test_clean_preserves_fragment():
    url = "https://example.com?utm_source=x#section"
    result = clean(url)
    assert "#section" in result


def test_clean_no_tracking():
    url = "https://example.com?q=test&page=2"
    result = clean(url)
    assert "q=test" in result
    assert "page=2" in result


def test_remove_specific_params():
    url = "https://example.com?a=1&b=2&c=3"
    result = remove_params(url, ["b", "c"])
    assert "a=1" in result
    assert "b=" not in result
    assert "c=" not in result


def test_normalize_lowercase():
    result = normalize("HTTPS://Example.COM/Path")
    assert result.startswith("https://example.com")


def test_normalize_sort_params():
    result = normalize("https://example.com?b=2&a=1")
    assert "a=1" in result
    assert result.index("a=1") < result.index("b=2")


def test_normalize_resolve_path():
    result = normalize("https://example.com/a/../b")
    assert "/b" in result
    assert ".." not in result


def test_clean_many():
    urls = [
        "https://example.com?utm_source=x",
        "https://test.com?fbclid=y&q=hello",
    ]
    results = clean_many(urls)
    assert len(results) == 2
    assert "utm_source" not in results[0]
    assert "q=hello" in results[1]


def test_clean_extra_params():
    url = "https://example.com?custom=1&id=2"
    result = clean(url, extra_params={"custom"})
    assert "custom" not in result
    assert "id=2" in result


def test_no_query_string():
    url = "https://example.com/page"
    assert clean(url) == url
