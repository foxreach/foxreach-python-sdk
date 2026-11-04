from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Lead:
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    status: str = "active"
    source: Optional[str] = None
    interest_status: Optional[str] = None
    interest_status_source: Optional[str] = None
    interest_status_updated_at: Optional[str] = None
    labels: List["LeadLabel"] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class LeadLabel:
    id: str
    name: str
    color: str = "neutral"
    meaning: str = "neutral"
    created_at: Optional[str] = None


@dataclass
class LeadCreate:
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


@dataclass
class LeadUpdate:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    interest_status: Optional[str] = None


@dataclass
class LeadListParams:
    page: int = 1
    page_size: int = 50
    search: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Campaign:
    id: str
    name: str
    status: str = "draft"
    timezone: str = "UTC"
    sending_days: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])
    sending_start_hour: int = 9
    sending_end_hour: int = 17
    daily_limit: int = 50
    esp_matching: bool = False
    sent_today: int = 0
    total_leads: int = 0
    total_sent: int = 0
    total_delivered: int = 0
    total_bounced: int = 0
    total_replied: int = 0
    total_opened: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class CampaignCreate:
    name: str
    timezone: str = "UTC"
    sending_days: Optional[List[int]] = None
    sending_start_hour: Optional[int] = None
    sending_end_hour: Optional[int] = None
    daily_limit: Optional[int] = None
    esp_matching: Optional[bool] = None


@dataclass
class CampaignUpdate:
    name: Optional[str] = None
    timezone: Optional[str] = None
    sending_days: Optional[List[int]] = None
    sending_start_hour: Optional[int] = None
    sending_end_hour: Optional[int] = None
    daily_limit: Optional[int] = None
    esp_matching: Optional[bool] = None


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Sequence:
    id: str
    campaign_id: str
    step_number: int = 1
    name: Optional[str] = None
    subject: Optional[str] = None
    body: str = ""
    delay_days: int = 0
    delay_hours: int = 0
    send_only_if_no_reply: bool = True
    send_as_html: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SequenceCreate:
    """Body of POST /campaigns/{id}/sequences.

    ``subject`` and ``body`` are required by the API. The step number is
    assigned by the server (next free step), so it cannot be set here.
    Fields left as ``None`` are omitted and take the server default.
    """

    body: str
    subject: str
    name: Optional[str] = None
    delay_days: int = 1
    delay_hours: Optional[int] = None
    send_only_if_no_reply: Optional[bool] = None
    send_as_html: Optional[bool] = None


@dataclass
class SequenceUpdate:
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    delay_days: Optional[int] = None
    delay_hours: Optional[int] = None
    send_only_if_no_reply: Optional[bool] = None
    send_as_html: Optional[bool] = None


@dataclass(frozen=True)
class SequenceVariant:
    """One A/B variant of a sequence step."""

    id: str
    sequence_id: str
    label: str
    subject: str = ""
    body: str = ""
    weight: int = 1
    send_as_html: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class VariantCreate:
    """Body of POST /campaigns/{id}/sequences/{sid}/variants."""

    subject: str
    body: str
    label: str = "A"
    weight: int = 1
    send_as_html: bool = False


@dataclass
class VariantUpdate:
    label: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    weight: Optional[int] = None
    send_as_html: Optional[bool] = None


@dataclass(frozen=True)
class VariantStats:
    """Per-variant results of one step. Rates are percentages."""

    variant_id: str
    label: str
    sent: int = 0
    opened: int = 0
    replied: int = 0
    bounced: int = 0
    open_rate: float = 0.0
    reply_rate: float = 0.0


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Template:
    id: str
    name: str
    subject: Optional[str] = None
    body: str = ""
    category: str = "email"
    send_as_html: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class TemplateCreate:
    """Body of POST /templates. ``category`` is omitted when ``None`` and the
    server stores ``"email"``; other values include ``"reply_macro"``."""

    name: str
    body: str
    subject: Optional[str] = None
    category: Optional[str] = None
    send_as_html: bool = False


@dataclass
class TemplateUpdate:
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    category: Optional[str] = None
    send_as_html: Optional[bool] = None


# ---------------------------------------------------------------------------
# Email Accounts
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EmailAccount:
    id: str
    email: str
    display_name: Optional[str] = None
    provider: Optional[str] = None
    daily_limit: int = 50
    sent_today: int = 0
    is_active: bool = True
    warmup_enabled: bool = False
    health_score: Optional[float] = None
    bounce_rate: Optional[float] = None
    reply_rate: Optional[float] = None
    connection_status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Inbox / Threads
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Thread:
    id: str
    from_email: Optional[str] = None
    to_email: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    body_plain: Optional[str] = None
    category: Optional[str] = None
    is_read: bool = False
    is_starred: bool = False
    campaign_id: Optional[str] = None
    lead_id: Optional[str] = None
    account_id: Optional[str] = None
    received_at: Optional[str] = None


@dataclass
class ThreadUpdate:
    category: Optional[str] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None


@dataclass
class ThreadListParams:
    page: int = 1
    page_size: int = 50
    category: Optional[str] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    account_id: Optional[str] = None
    campaign_id: Optional[str] = None
    search: Optional[str] = None


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OverviewStats:
    total_accounts: int = 0
    active_accounts: int = 0
    total_campaigns: int = 0
    active_campaigns: int = 0
    total_leads: int = 0
    total_sent: int = 0
    total_replies: int = 0
    reply_rate: float = 0.0
    # Average Health Score over accounts that have one; None when none are measured yet.
    account_health_avg: Optional[float] = None


@dataclass(frozen=True)
class DailyStat:
    date: str = ""
    sent: int = 0
    delivered: int = 0
    bounced: int = 0
    replied: int = 0
    opened: int = 0


@dataclass(frozen=True)
class CampaignAnalytics:
    sent: int = 0
    delivered: int = 0
    bounced: int = 0
    replied: int = 0
    opened: int = 0
    reply_rate: float = 0.0
    bounce_rate: float = 0.0
    daily_stats: List[DailyStat] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Webhook Events
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class WebhookEvent:
    id: str
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Webhook:
    id: str
    url: str
    is_active: bool = True
    events: List[str] = field(default_factory=list)
    secret: Optional[str] = None
    last_delivered_at: Optional[str] = None
    consecutive_failures: int = 0
    reply_categories: Optional[List[str]] = None
    paused_at: Optional[str] = None
    paused_reason: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class WebhookCreate:
    url: str
    events: List[str]
    is_active: bool = True
    reply_categories: Optional[List[str]] = None


@dataclass
class WebhookUpdate:
    url: Optional[str] = None
    events: Optional[List[str]] = None
    is_active: Optional[bool] = None
    reply_categories: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# Pagination Meta
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PaginationMeta:
    page: int = 1
    page_size: int = 50
    total: int = 0
    total_pages: int = 0


# ---------------------------------------------------------------------------
# Email Account Create / Update / Reconnect
# ---------------------------------------------------------------------------

@dataclass
class EmailAccountCreate:
    email: str
    password: str
    smtp_host: str
    smtp_port: int
    imap_host: str
    imap_port: int
    provider: str = "other"
    display_name: Optional[str] = None
    timezone: Optional[str] = None
    daily_limit: Optional[int] = None
    warmup_enabled: Optional[bool] = None
    warmup_daily_limit: Optional[int] = None
    warmup_ramp_up_days: Optional[int] = None


@dataclass
class EmailAccountUpdate:
    display_name: Optional[str] = None
    daily_limit: Optional[int] = None
    timezone: Optional[str] = None
    warmup_enabled: Optional[bool] = None
    warmup_daily_limit: Optional[int] = None
    warmup_ramp_up_days: Optional[int] = None
    is_active: Optional[bool] = None


@dataclass
class ReconnectRequest:
    password: str


# ---------------------------------------------------------------------------
# Health Payload
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HealthPayload:
    health_score: Optional[int] = None
    health_basis: Optional[Dict[str, Any]] = None
    bounce_7d: Optional[Dict[str, Any]] = None
    warmup_enabled: Optional[bool] = None
    warmup_progress: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Warmup
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class WarmupPoolEntry:
    account_id: str = ""
    email: str = ""
    display_name: Optional[str] = None
    health_score: Optional[int] = None
    health_basis: Optional[Dict[str, Any]] = None
    warmup_enabled: bool = False
    warmup_progress: Optional[Dict[str, Any]] = None
    pool_stats: Optional[Dict[str, Any]] = None
    tags: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class WarmupStats:
    total_accounts: int = 0
    active_warmup_accounts: int = 0
    total_sent: int = 0
    total_replied: int = 0
    average_health_score: Optional[float] = None
    health_measured_accounts: int = 0


@dataclass(frozen=True)
class WarmupLog:
    id: str = ""
    sender_email: str = ""
    receiver_email: str = ""
    subject: Optional[str] = None
    status: Optional[str] = None
    replied_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass(frozen=True)
class WarmupTag:
    id: str = ""
    name: str = ""
    color: Optional[str] = None


# ---------------------------------------------------------------------------
# Tracking Domains
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TrackingDomain:
    id: str = ""
    domain: str = ""
    status: str = "pending"
    cname_target: Optional[str] = None
    cf_hostname_id: Optional[str] = None
    failure_reason: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class TrackingDomainCreate:
    domain: str


# ---------------------------------------------------------------------------
# Block list
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BlockListEntry:
    id: str = ""
    kind: str = "email"  # email | domain
    value: str = ""
    source: str = "manual"  # manual | import | unsubscribe | api
    note: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None


@dataclass(frozen=True)
class BlockListBulkResult:
    created: int = 0
    duplicates: int = 0
    invalid: int = 0
    invalid_details: List[Dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Managed Inboxes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ManagedInboxConfig:
    platforms: List[Dict[str, Any]] = field(default_factory=list)
    max_mailboxes_per_domain: int = 0
    max_domains_per_order: int = 0
    registration_years: int = 1
    default_daily_limit: int = 0


@dataclass(frozen=True)
class ManagedOrder:
    id: str = ""
    status: str = ""
    platform: Optional[str] = None
    total_cents: int = 0
    domains: List[Dict[str, Any]] = field(default_factory=list)
    mailboxes: List[Dict[str, Any]] = field(default_factory=list)
    created_at: Optional[str] = None


@dataclass(frozen=True)
class ManagedMailbox:
    id: str = ""
    email: str = ""
    domain: Optional[str] = None
    platform: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Lead Finder
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LeadFinderCredits:
    balance: int = 0
    expires_at: Optional[str] = None
    monthly_included: int = 0
    allowed_countries: List[str] = field(default_factory=list)
    blocked_countries: List[str] = field(default_factory=list)
    coverage: Optional[str] = None
    credits_per_pack: int = 0
    price_per_pack_cents: int = 0
    search_pages_used_today: int = 0
    search_pages_allowed_today: int = 0
    search_pages_per_reveal: int = 0


@dataclass(frozen=True)
class RevealBatch:
    batch_id: str = ""
    reveals: List[Dict[str, Any]] = field(default_factory=list)
    pending: int = 0
    found: int = 0
    not_found: int = 0
    errors: int = 0
    balance: int = 0


@dataclass(frozen=True)
class LeadFinderList:
    id: str = ""
    name: str = ""
    kind: Optional[str] = None
    item_count: int = 0
    created_at: Optional[str] = None


@dataclass(frozen=True)
class LeadFinderSavedSearch:
    id: str = ""
    name: str = ""
    filters: Optional[Dict[str, Any]] = None
    last_count: Optional[int] = None
    created_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Lead Tags
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LeadTag:
    name: str = ""
    count: int = 0


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------


@dataclass
class Job:
    id: str
    type: str
    status: str
    progress: int = 0
    total_items: int = 0
    completed_items: int = 0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Me
# ---------------------------------------------------------------------------


@dataclass
class Me:
    """The calling API key, its workspace, plan, per-class rate limits and credits.

    The nested dicts use snake_case keys like the rest of the SDK
    (``plan["limits"]["monthly_email_limit"]``, ``credits["lead_finder"]["balance"]``).
    """

    key: Dict[str, Any] = field(default_factory=dict)
    workspace: Dict[str, Any] = field(default_factory=dict)
    plan: Dict[str, Any] = field(default_factory=dict)
    rate_limit: Dict[str, Any] = field(default_factory=dict)
    credits: Dict[str, Any] = field(default_factory=dict)
