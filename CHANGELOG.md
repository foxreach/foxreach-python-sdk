# Changelog

## [0.5.0] - 2026-11-03

### Added

- `leads.list(provider=...)` (sync and async): filter leads by the recipient's mail provider (`google`, `microsoft`, `zoho`, `yahoo`, `godaddy`, `other`, `gateway`, `unresolved`) against `GET /leads?provider=`. `gateway` means the mail goes through a security gateway such as Proofpoint or Mimecast.
- `leads.providers()` (sync and async): `GET /leads/providers`, the count of live leads per mail provider, the gateway count, the total and the share already checked.
- `campaigns.get_esp_mix(campaign_id)` (sync and async): `GET /campaigns/{id}/esp-mix`, the split of a campaign's mailboxes and leads across Google, Microsoft and other providers.

## [0.4.2] - 2026-10-21

### Added

- `leads.list(email=...)` (sync and async): exact, case-insensitive email match against `GET /leads?email=`. `%` and `_` are literal, unlike `search`, which matches substrings.
- `inbox.get(reply_id, mark_read=False)` (sync and async): sends `markRead=true` only when `mark_read=True`.
- `SequenceCreate` / `SequenceUpdate`: `name`, `delay_hours`, `send_only_if_no_reply`, `send_as_html`, matching the backend `SequenceCreateRequest` / `SequenceUpdateRequest`.
- `Sequence`: `name`, `delay_hours`, `send_only_if_no_reply`, `send_as_html` are now read from the response.

### Changed

- Reading a thread no longer marks it read. `GET /inbox/threads/{id}` stopped marking threads read by default; `inbox.get()` now does the same and only marks a thread read when you pass `mark_read=True`. Code that relied on `get()` to clear the unread flag must pass `mark_read=True` or call `inbox.update(..., ThreadUpdate(is_read=True))`.
- `SequenceCreate.subject` is now required. The API rejects a sequence step without a subject (422), so the SDK no longer lets you build one.
- `SequenceCreate.step_number`, `SequenceCreate.template_type` and `SequenceUpdate.step_number` are removed. The API never accepted them: the step number is assigned by the server and sequences have no template type, so both were silently dropped. Passing them now raises `TypeError`.
- Templates use `category` (the API field) instead of `template_type`: `TemplateCreate.category`, `TemplateUpdate.category` and `Template.category`. Before this, `template_type` was sent as `templateType`, which the API ignored, so every template was stored as `email`; and `Template.template_type` was read from a key the API never returns, so it always said `email`.
- `Sequence.template_type` is removed (the API never returned it).

### Fixed

- Version sources agree: `pyproject.toml` and `foxreach/_version.py` both say 0.4.2, and a test asserts it (`tests/test_request_shapes.py::test_pyproject_version_matches_dunder_version`).

## [0.4.1] - 2026-10-21

### Fixed

- `AsyncInboxResource.categorize_stats`: parameter was `sequence_id: str` with key `sequenceId`; corrected to `sequence_step: int` with key `sequenceStep` to match the backend `GET /inbox/categorize-stats` query parameter. The wrong parameter was silently dropped by the backend, so filters were never applied.
- `_keys_to_camel` and `_keys_to_snake` in `_http.py` no longer recurse into values under `custom_fields`/`customFields` keys. Previously, a user custom field like `{"company_size": 50}` was silently renamed to `{"companySize": 50}` on the wire, and received as `{"company_size": 50}` on parse -- losing the original key. User-controlled keys inside `customFields` are now preserved as-is in both directions.

## [0.4.0] - 2026-10-21

### Added
- Full coverage of all public REST v1 endpoints
- New resources: `warmup`, `lead_finder`, `managed_inboxes`, `tracking_domains`
- New methods on `email_accounts`: `create`, `update`, `reconnect`, `enable_warmup`, `disable_warmup`, `health`, `warmup_detail`, `google_oauth_start`
- New method on `leads`: `list_tags`
- New method on `inbox`: `delete`
- New types: `EmailAccountCreate`, `EmailAccountUpdate`, `ReconnectRequest`, `HealthPayload`, `WarmupPoolEntry`, `WarmupStats`, `WarmupLog`, `WarmupTag`, `TrackingDomain`, `TrackingDomainCreate`, `ManagedInboxConfig`, `ManagedOrder`, `ManagedMailbox`, `LeadFinderCredits`, `RevealBatch`, `LeadFinderList`, `LeadFinderSavedSearch`, `LeadTag`
- Nullable health fields: `healthScore` (`Optional[int]`), `averageHealthScore` (`Optional[float]`), `healthBasis`, `healthMeasuredAccounts` — null until 20 warmup sends are measured
- Both sync (`FoxReach`) and async (`AsyncFoxReach`) clients expose all new resources

### Fixed
- Single version source: `__version__` in `foxreach/__init__.py` now drives both `pyproject.toml` and the User-Agent header; `_http.py` imports `__version__` instead of hardcoding `"0.1.0"`
- Version bumped from inconsistent 0.1.0/0.2.0/0.3.0 to unified 0.4.0

### Notes
- PyPI publishing is pending; not yet published to pypi.org
