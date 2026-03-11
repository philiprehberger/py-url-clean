# philiprehberger-url-clean

Remove tracking parameters from URLs.

## Installation

```bash
pip install philiprehberger-url-clean
```

## Usage

```python
from philiprehberger_url_clean import clean, remove_params, normalize

# Remove tracking params (utm_*, fbclid, gclid, etc.)
clean("https://example.com/page?utm_source=twitter&id=123")
# "https://example.com/page?id=123"

# Remove specific params
remove_params("https://example.com?a=1&b=2&c=3", ["b", "c"])
# "https://example.com?a=1"

# Normalize URL
normalize("HTTPS://Example.COM/path/../page?b=2&a=1")
# "https://example.com/page?a=1&b=2"

# Batch processing
clean_many(["https://example.com?utm_source=x", ...])
```

## API

- `clean(url, extra_params=None)` — Remove known tracking parameters
- `remove_params(url, params)` — Remove specific parameters
- `normalize(url)` — Lowercase host, sort params, resolve path
- `clean_many(urls, extra_params=None)` — Batch clean

## License

MIT
