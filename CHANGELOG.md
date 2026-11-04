# Changelog

## [Unreleased]

## [0.6.0] - 2026-11-04

Covers all 203 operations of the public API v1 (0.5.0 covered 90).

### Added

- `leads.bulk_delete`, `bulk_delete_impact`, `bulk_tag`, `bulk_untag`, `bulk_verify`, `export`, `download_export` and `variables` (sync and async): bulk lead actions by `lead_ids` or `filter` (each returns a `Job`), a CSV export job with a download, and the merge-tag list. `bulk_delete` is irreversible for campaign membership; `bulk_verify` spends verification credits.
- `workspace` resource (`get`, `update`, `members`, `invite`, `update_member_role`, `remove_member`, `invites`, `revoke_invite`, `resend_invite`, `defaults`, `update_defaults`) and `api_keys` resource (`list`, `create`, `revoke`), sync and async. Team changes and API key management need a key with the new opt-in `admin` scope.
- `webhooks.test(id)`, `webhooks.deliveries(id, status=...)` and the `events` resource (`events.list(type, start_date, end_date)`), sync and async: `POST /webhooks/{id}/test`, `GET /webhooks/{id}/deliveries`, `GET /events`.
- `inbox.mark_read`, `mark_all_read`, `bulk_update`, `bulk_delete`, `list_notes`, `add_note`, `delete_note`, `list_sent` (sync and async): `/inbox/threads/{id}/mark-read`, `/inbox/mark-all-read`, `/inbox/threads/bulk-update`, `/inbox/threads/bulk-delete`, `/inbox/threads/{id}/notes`, `/inbox/notes/{id}`, `/inbox/sent`. Bulk calls take up to 100 ids.
- `agency` resource (sync and async): `overview`, `list_clients`, `create_client`, `rename_client`, `delete_client`, `get_branding`, `update_branding` against `/agency/*`. Agency keys only; changes need a key created by the agency owner.
- `audit_log.list(...)`: `GET /audit-log`, one page of who or what changed state, filtered by source, actor, time, campaign or account; pass `meta.next_cursor` as `cursor` for the next page.
- `analytics`: `account`, `report`, `export_report` (CSV text), `leaderboard`, `activity`, `campaign_daily`, `campaign_steps`.
- `lead_finder`: `create_list`, `get_list`, `rename_list`, `delete_list`, `list_items`, `add_items`, `remove_items`, `reveal_list` (spends reveal credits), `add_list_to_leads`, `export_list`, `create_saved_search`, `get_saved_search`, `update_saved_search`, `delete_saved_search`, `run_saved_search` (free).
- `warmup`: `create_tag`, `update_tag`, `delete_tag`, `assign_tag`, `unassign_tag`.
- `email_accounts`: `test_connection` (SMTP and IMAP probe, public mail hosts only) and `check_domain_auth`.
- `templates`: `publish`, `unpublish`, `clone`.
These methods return the API's `data` as a plain dict or list (keys in snake_case).

- `FoxReach(workspace_id=...)` and `AsyncFoxReach(workspace_id=...)`: act as a client workspace of an Agency key (sends `X-Workspace-Id`).
- `workspaces.list()` (sync and async): `GET /workspaces`, the workspaces the key can act as.
- `client.me()` (sync and async): `GET /me`, the calling key, its workspace, the plan and limits, the rate limit and the credit balances. Returns `Me`.
- `jobs.list(type=..., status=...)` and `jobs.get(job_id)` (sync and async): `GET /jobs` and `GET /jobs/{job_id}`, the status, progress and result counters of background jobs (lead imports, verification runs). Returns `Job`.
- `block_list` resource (sync and async): `list`, `add`, `bulk_add`, `remove`, `bulk_remove`, `export` against `/block-list`. Types `BlockListEntry` and `BlockListBulkResult`.
- `leads.bulk_import()` result gains `blocked` and `blocked_emails`: rows skipped because the address or domain is on the block list. `campaigns.add_leads()` returns `blocked` alongside `added` and `skipped`.

- `campaigns.duplicate`, `share`, `unshare`, `preview`, `send_test_email`, `bulk_remove_leads`, `activity`, `cohorts`, `cohort_detail` and `lead_emails` (sync and async). `send_test_email` sends one real email; `bulk_remove_leads` takes up to 5,000 ids on a campaign that is not active.
- A/B variants on sequence steps: `campaigns.sequences.list_variants`, `create_variant`, `update_variant`, `delete_variant` and `variant_stats` (sync and async), with the types `SequenceVariant`, `VariantCreate`, `VariantUpdate` and `VariantStats`. Variants cannot be added while the campaign is active.
- `inbox.drafts` (sync and async): `list`, `get`, `update`, `send`, `regenerate`, `dismiss` for AI reply drafts. `send` sends the stored draft as a real email.
- `lead_labels` resource (sync and async): `list`, `create`, `update`, `delete`, `assign`, `unassign`. Type `LeadLabel`; `Lead` gains `labels`, `interest_status`, `interest_status_source` and `interest_status_updated_at`.
- `leads.set_interest_status(lead_id, status)` (sync and async): set or clear the interest status by hand; `LeadUpdate` gains `interest_status`.
- `copy.judge` (free) and `copy.rewrite` (1 AI credit) (sync and async): `POST /copy/judge` and `POST /copy/rewrite`.
- `webhooks.resume(id)` (sync and async): turn a webhook that was paused after 10 failed deliveries in a row back on. `Webhook` gains `paused_at` and `paused_reason`; `Webhook`, `WebhookCreate` and `WebhookUpdate` gain `reply_categories`.

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
