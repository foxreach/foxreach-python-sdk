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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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


@dataclass
class CampaignUpdate:
    name: Optional[str] = None
    timezone: Optional[str] = None
    sending_days: Optional[List[int]] = None
    sending_start_hour: Optional[int] = None
    sending_end_hour: Optional[int] = None
    daily_limit: Optional[int] = None


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Sequence:
    id: str
    campaign_id: str
    step_number: int = 1
    subject: Optional[str] = None
    body: str = ""
    delay_days: int = 1
    template_type: str = "email"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SequenceCreate:
    body: str
    subject: Optional[str] = None
    delay_days: int = 1
    step_number: Optional[int] = None
    template_type: str = "email"


@dataclass
class SequenceUpdate:
    subject: Optional[str] = None
    body: Optional[str] = None
    delay_days: Optional[int] = None
    step_number: Optional[int] = None


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Template:
    id: str
    name: str
    subject: Optional[str] = None
    body: str = ""
    template_type: str = "email"
    send_as_html: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class TemplateCreate:
    name: str
    body: str
    subject: Optional[str] = None
    template_type: str = "email"
    send_as_html: bool = False


@dataclass
class TemplateUpdate:
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    template_type: Optional[str] = None
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
    account_health_avg: float = 0.0


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
# Pagination Meta
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PaginationMeta:
    page: int = 1
    page_size: int = 50
    total: int = 0
    total_pages: int = 0
