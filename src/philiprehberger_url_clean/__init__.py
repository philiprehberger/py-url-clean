"""Remove tracking parameters from URLs."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse, urlencode, parse_qs


__all__ = [
    "clean",
    "clean_url",
    "remove_params",
    "normalize",
    "clean_many",
    "register_tracking_param",
    "unregister_tracking_param",
    "TRACKING_PARAMS",
]

TRACKING_PARAMS: set[str] = {
    # Google
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_source_platform", "utm_creative_format", "utm_marketing_tactic",
    "gclid", "gclsrc", "dclid", "gbraid", "wbraid",
    # Facebook / Meta
    "fbclid", "fb_action_ids", "fb_action_types", "fb_source", "fb_ref",
    # Microsoft / Bing
    "msclkid",
    # Mailchimp
    "mc_cid", "mc_eid",
    # HubSpot
    "_hsenc", "_hsmi", "hsa_cam", "hsa_grp", "hsa_mt", "hsa_src",
    "hsa_ad", "hsa_acc", "hsa_net", "hsa_ver", "hsa_la", "hsa_ol",
    "hsa_kw", "hsa_tgt",
    # Adobe
    "s_cid", "ef_id",
    # Misc tracking
    "ref", "ref_src", "ref_url",
    "igshid", "si", "feature", "trk",
    "_ga", "_gl", "_ke",
}

def clean(url: str, *, extra_params: set[str] | None = None) -> str:
    """Remove known tracking parameters from a URL.

    Args:
        url: The URL to clean.
        extra_params: Additional parameter names to remove.

    Returns:
        URL with tracking parameters removed.
    """
    params_to_remove = TRACKING_PARAMS | (extra_params or set())
    cleaned, _ = _strip_params(url, params_to_remove)
    return cleaned


def clean_url(url: str, *, extra_params: set[str] | None = None) -> tuple[str, list[str]]:
    """Remove tracking parameters and return both the cleaned URL and the names removed.

    Args:
        url: The URL to clean.
        extra_params: Additional parameter names to remove.

    Returns:
        Tuple of ``(cleaned_url, removed_params)`` where ``removed_params`` is the
        sorted list of parameter names that were stripped.
    """
    params_to_remove = TRACKING_PARAMS | (extra_params or set())
    return _strip_params(url, params_to_remove)


def register_tracking_param(name: str) -> None:
    """Add *name* to the global set of tracking parameters.

    Subsequent calls to :func:`clean` and :func:`clean_url` will strip it.
    """
    TRACKING_PARAMS.add(name)


def unregister_tracking_param(name: str) -> None:
    """Remove *name* from the global set of tracking parameters (no-op if absent)."""
    TRACKING_PARAMS.discard(name)


def remove_params(url: str, params: list[str] | set[str]) -> str:
    """Remove specific parameters from a URL.

    Args:
        url: The URL to modify.
        params: Parameter names to remove.

    Returns:
        URL with specified parameters removed.
    """
    cleaned, _ = _strip_params(url, set(params))
    return cleaned


def normalize(url: str) -> str:
    """Normalize a URL: lowercase scheme/host, sort params, resolve path.

    Args:
        url: The URL to normalize.

    Returns:
        Normalized URL.
    """
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Resolve relative path components
    path = _resolve_path(parsed.path) or "/"

    # Sort query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_params = sorted(query_params.items())
    query = urlencode(
        [(k, v[0]) if len(v) == 1 else (k, v) for k, v in sorted_params],
        doseq=True,
    )

    return urlunparse((scheme, netloc, path, parsed.params, query, parsed.fragment))


def clean_many(urls: list[str], *, extra_params: set[str] | None = None) -> list[str]:
    """Clean tracking parameters from multiple URLs.

    Args:
        urls: List of URLs.
        extra_params: Additional parameter names to remove.

    Returns:
        List of cleaned URLs.
    """
    return [clean(url, extra_params=extra_params) for url in urls]


def _strip_params(url: str, params_to_remove: set[str]) -> tuple[str, list[str]]:
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query, keep_blank_values=True)

    filtered = {k: v for k, v in query_params.items() if k not in params_to_remove}
    removed = sorted(k for k in query_params if k in params_to_remove)

    query = urlencode(
        [(k, v[0]) if len(v) == 1 else (k, v) for k, v in filtered.items()],
        doseq=True,
    )

    cleaned = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, query, parsed.fragment))
    return cleaned, removed


def _resolve_path(path: str) -> str:
    parts = path.split("/")
    resolved: list[str] = []
    for part in parts:
        if part == "..":
            if resolved and resolved[-1] != "":
                resolved.pop()
        elif part != ".":
            resolved.append(part)
    return "/".join(resolved)
