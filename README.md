# philiprehberger-url-clean

[![Tests](https://github.com/philiprehberger/py-url-clean/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-url-clean/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-url-clean.svg)](https://pypi.org/project/philiprehberger-url-clean/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-url-clean)](https://github.com/philiprehberger/py-url-clean/commits/main)

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

# Get the list of stripped params alongside the cleaned URL
from philiprehberger_url_clean import clean_url, register_tracking_param

cleaned, removed = clean_url("https://example.com?utm_source=x&id=1")
# cleaned = "https://example.com?id=1"
# removed = ["utm_source"]

# Add a custom tracking param at runtime
register_tracking_param("internal_ref")
clean("https://example.com?internal_ref=abc&id=1")
# "https://example.com?id=1"
```

## API

| Function / Class | Description |
|------------------|-------------|
| `clean(url, extra_params=None)` | Remove known tracking parameters |
| `clean_url(url, extra_params=None)` | Returns `(cleaned_url, removed_params)` tuple |
| `remove_params(url, params)` | Remove specific parameters |
| `normalize(url)` | Lowercase host, sort params, resolve path |
| `clean_many(urls, extra_params=None)` | Batch clean |
| `register_tracking_param(name)` | Add a parameter to the global tracking set |
| `unregister_tracking_param(name)` | Remove a parameter from the global tracking set |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-url-clean)

🐛 [Report issues](https://github.com/philiprehberger/py-url-clean/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-url-clean/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
