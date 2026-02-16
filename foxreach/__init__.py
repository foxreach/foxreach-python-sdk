"""FoxReach — Official Python SDK for the FoxReach cold email outreach API."""

from .client import AsyncFoxReach, FoxReach
from ._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    FoxReachError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .types import (
    Campaign,
    CampaignAnalytics,
    CampaignCreate,
    CampaignUpdate,
    DailyStat,
    EmailAccount,
    Lead,
    LeadCreate,
    LeadListParams,
    LeadUpdate,
    OverviewStats,
    PaginationMeta,
    Sequence,
    SequenceCreate,
    SequenceUpdate,
    Template,
    TemplateCreate,
    TemplateUpdate,
    Thread,
    ThreadListParams,
    ThreadUpdate,
    WebhookEvent,
)

__version__ = "0.1.0"

__all__ = [
    # Clients
    "FoxReach",
    "AsyncFoxReach",
    # Exceptions
    "FoxReachError",
    "AuthenticationError",
    "BadRequestError",
    "ConnectionError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    # Types
    "Campaign",
    "CampaignAnalytics",
    "CampaignCreate",
    "CampaignUpdate",
    "DailyStat",
    "EmailAccount",
    "Lead",
    "LeadCreate",
    "LeadListParams",
    "LeadUpdate",
    "OverviewStats",
    "PaginationMeta",
    "Sequence",
    "SequenceCreate",
    "SequenceUpdate",
    "Template",
    "TemplateCreate",
    "TemplateUpdate",
    "Thread",
    "ThreadListParams",
    "ThreadUpdate",
    "WebhookEvent",
]
