from __future__ import annotations

from ._http import AsyncHttpClient, HttpClient
from .resources.leads import AsyncLeadsResource, LeadsResource
from .resources.lead_labels import AsyncLeadLabelsResource, LeadLabelsResource
from .resources.campaigns import AsyncCampaignsResource, CampaignsResource
from .resources.templates import AsyncTemplatesResource, TemplatesResource
from .resources.email_accounts import AsyncEmailAccountsResource, EmailAccountsResource
from .resources.inbox import AsyncInboxResource, InboxResource
from .resources.analytics import AsyncAnalyticsResource, AnalyticsResource
from .resources.webhooks import AsyncWebhooksResource, WebhooksResource
from .resources.events import AsyncEventsResource, EventsResource
from .resources.workspace import AsyncWorkspaceResource, WorkspaceResource
from .resources.api_keys import AsyncApiKeysResource, ApiKeysResource
from .resources.copy import AsyncCopyResource, CopyResource
from .resources.verification import AsyncVerificationResource, VerificationResource
from .resources.warmup import AsyncWarmupResource, WarmupResource
from .resources.lead_finder import AsyncLeadFinderResource, LeadFinderResource
from .resources.managed_inboxes import AsyncManagedInboxesResource, ManagedInboxesResource
from .resources.me import make_me
from .types import Me
from .resources.jobs import AsyncJobsResource, JobsResource
from .resources.block_list import AsyncBlockListResource, BlockListResource
from .resources.tracking_domains import AsyncTrackingDomainsResource, TrackingDomainsResource
from .resources.workspaces import AsyncWorkspacesResource, WorkspacesResource
from .resources.audit_log import AsyncAuditLogResource, AuditLogResource
from .resources.agency import AsyncAgencyResource, AgencyResource

_DEFAULT_BASE_URL = "https://api.foxreach.io/api/v1"


class FoxReach:
    """Synchronous FoxReach API client.

    Usage::

        from foxreach import FoxReach

        client = FoxReach(api_key="otr_...")
        leads = client.leads.list(search="jane")
        for lead in leads:
            print(lead.email)

    An agency key can act as a client workspace: pass ``workspace_id`` (see
    ``client.workspaces.list()`` for the ids the key can use).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        workspace_id: str | None = None,
    ) -> None:
        if not api_key or not api_key.startswith("otr_"):
            raise ValueError('API key must start with "otr_"')

        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            workspace_id=workspace_id,
        )

        self.leads = LeadsResource(self._http)
        self.lead_labels = LeadLabelsResource(self._http)
        self.campaigns = CampaignsResource(self._http)
        self.templates = TemplatesResource(self._http)
        self.email_accounts = EmailAccountsResource(self._http)
        self.inbox = InboxResource(self._http)
        self.analytics = AnalyticsResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.verification = VerificationResource(self._http)
        self.copy = CopyResource(self._http)
        self.warmup = WarmupResource(self._http)
        self.lead_finder = LeadFinderResource(self._http)
        self.managed_inboxes = ManagedInboxesResource(self._http)
        self.tracking_domains = TrackingDomainsResource(self._http)
        self.block_list = BlockListResource(self._http)
        self.events = EventsResource(self._http)
        self.workspace = WorkspaceResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.workspaces = WorkspacesResource(self._http)
        self.jobs = JobsResource(self._http)
        self.audit_log = AuditLogResource(self._http)
        self.agency = AgencyResource(self._http)

    def me(self) -> Me:
        """Describe the calling API key: key, workspace, plan, rate limit and credits."""
        return make_me(self._http.request("GET", "/me"))

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> FoxReach:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncFoxReach:
    """Async FoxReach API client.

    Usage::

        from foxreach import AsyncFoxReach

        async with AsyncFoxReach(api_key="otr_...") as client:
            leads = await client.leads.list(search="jane")
            async for lead in leads.auto_paging_iter():
                print(lead.email)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        workspace_id: str | None = None,
    ) -> None:
        if not api_key or not api_key.startswith("otr_"):
            raise ValueError('API key must start with "otr_"')

        self._http = AsyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            workspace_id=workspace_id,
        )

        self.leads = AsyncLeadsResource(self._http)
        self.lead_labels = AsyncLeadLabelsResource(self._http)
        self.campaigns = AsyncCampaignsResource(self._http)
        self.templates = AsyncTemplatesResource(self._http)
        self.email_accounts = AsyncEmailAccountsResource(self._http)
        self.inbox = AsyncInboxResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)
        self.verification = AsyncVerificationResource(self._http)
        self.copy = AsyncCopyResource(self._http)
        self.warmup = AsyncWarmupResource(self._http)
        self.lead_finder = AsyncLeadFinderResource(self._http)
        self.managed_inboxes = AsyncManagedInboxesResource(self._http)
        self.tracking_domains = AsyncTrackingDomainsResource(self._http)
        self.block_list = AsyncBlockListResource(self._http)
        self.events = AsyncEventsResource(self._http)
        self.workspace = AsyncWorkspaceResource(self._http)
        self.api_keys = AsyncApiKeysResource(self._http)
        self.workspaces = AsyncWorkspacesResource(self._http)
        self.jobs = AsyncJobsResource(self._http)
        self.audit_log = AsyncAuditLogResource(self._http)
        self.agency = AsyncAgencyResource(self._http)

    async def me(self) -> Me:
        """Describe the calling API key: key, workspace, plan, rate limit and credits."""
        return make_me(await self._http.request("GET", "/me"))

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> AsyncFoxReach:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
