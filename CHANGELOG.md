# Changelog

## 0.2.0 (2026-04-27)

- Add `clean_url()` returning `(cleaned_url, removed_params)` tuple for audit/logging use cases
- Add `register_tracking_param()` and `unregister_tracking_param()` to extend the global tracking-param set at runtime
- Remove dead code branch in `_strip_params` and an unused private constant
- Repair malformed CHANGELOG entries from previous releases

## 0.1.6 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.5 (2026-03-22)

- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.4 (2026-03-15)

- Add Development section to README

## 0.1.1 (2026-03-12)

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)

- Initial release
