from __future__ import annotations

from ._http import AsyncHttpClient, HttpClient
from .resources.leads import AsyncLeadsResource, LeadsResource
from .resources.campaigns import AsyncCampaignsResource, CampaignsResource
from .resources.templates import AsyncTemplatesResource, TemplatesResource
from .resources.email_accounts import AsyncEmailAccountsResource, EmailAccountsResource
from .resources.inbox import AsyncInboxResource, InboxResource
from .resources.analytics import AsyncAnalyticsResource, AnalyticsResource
from .resources.webhooks import AsyncWebhooksResource, WebhooksResource
from .resources.verification import AsyncVerificationResource, VerificationResource
from .resources.warmup import AsyncWarmupResource, WarmupResource
from .resources.lead_finder import AsyncLeadFinderResource, LeadFinderResource
from .resources.managed_inboxes import AsyncManagedInboxesResource, ManagedInboxesResource
from .resources.tracking_domains import AsyncTrackingDomainsResource, TrackingDomainsResource

_DEFAULT_BASE_URL = "https://api.foxreach.io/api/v1"


class FoxReach:
    """Synchronous FoxReach API client.

    Usage::

        from foxreach import FoxReach

        client = FoxReach(api_key="otr_...")
        leads = client.leads.list(search="jane")
        for lead in leads:
            print(lead.email)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        if not api_key or not api_key.startswith("otr_"):
            raise ValueError('API key must start with "otr_"')

        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.leads = LeadsResource(self._http)
        self.campaigns = CampaignsResource(self._http)
        self.templates = TemplatesResource(self._http)
        self.email_accounts = EmailAccountsResource(self._http)
        self.inbox = InboxResource(self._http)
        self.analytics = AnalyticsResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.verification = VerificationResource(self._http)
        self.warmup = WarmupResource(self._http)
        self.lead_finder = LeadFinderResource(self._http)
        self.managed_inboxes = ManagedInboxesResource(self._http)
        self.tracking_domains = TrackingDomainsResource(self._http)

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
    ) -> None:
        if not api_key or not api_key.startswith("otr_"):
            raise ValueError('API key must start with "otr_"')

        self._http = AsyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.leads = AsyncLeadsResource(self._http)
        self.campaigns = AsyncCampaignsResource(self._http)
        self.templates = AsyncTemplatesResource(self._http)
        self.email_accounts = AsyncEmailAccountsResource(self._http)
        self.inbox = AsyncInboxResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)
        self.verification = AsyncVerificationResource(self._http)
        self.warmup = AsyncWarmupResource(self._http)
        self.lead_finder = AsyncLeadFinderResource(self._http)
        self.managed_inboxes = AsyncManagedInboxesResource(self._http)
        self.tracking_domains = AsyncTrackingDomainsResource(self._http)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> AsyncFoxReach:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
