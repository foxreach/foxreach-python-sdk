# FoxReach Python SDK

Official Python SDK for the [FoxReach](https://foxreach.io) cold email outreach API.

## Installation

```bash
pip install foxreach
```

## Quick Start

```python
from foxreach import FoxReach, LeadCreate

client = FoxReach(api_key="otr_your_api_key")

# Create a lead
lead = client.leads.create(LeadCreate(
    email="jane@example.com",
    first_name="Jane",
    last_name="Smith",
    company="Acme Corp",
))

# List leads with pagination
page = client.leads.list(search="jane", page_size=25)
for lead in page:
    print(lead.email)

# Auto-paginate through all results
for lead in client.leads.list().auto_paging_iter():
    print(lead.email)
```

## Async Support

```python
from foxreach import AsyncFoxReach, LeadCreate

async with AsyncFoxReach(api_key="otr_your_api_key") as client:
    lead = await client.leads.create(LeadCreate(email="jane@example.com"))

    async for lead in (await client.leads.list()).auto_paging_iter():
        print(lead.email)
```

## Resources

### Leads

```python
client.leads.list(page=1, page_size=50, search="...", status="active", tags="...")
client.leads.list(email="jane@example.com")  # exact, case-insensitive match
client.leads.get("cld_...")
client.leads.create(LeadCreate(email="..."))
client.leads.update("cld_...", LeadUpdate(company="New Co"))
client.leads.delete("cld_...")
```

### Campaigns

```python
client.campaigns.list(status="active")
client.campaigns.get("cmp_...")
client.campaigns.create(CampaignCreate(name="Q1 Outreach"))
client.campaigns.update("cmp_...", CampaignUpdate(daily_limit=100))
client.campaigns.delete("cmp_...")
client.campaigns.start("cmp_...")
client.campaigns.pause("cmp_...")
client.campaigns.add_leads("cmp_...", ["cld_1", "cld_2"])
client.campaigns.add_accounts("cmp_...", ["acc_1"])
```

### Sequences

```python
client.campaigns.sequences.list("cmp_...")
client.campaigns.sequences.create("cmp_...", SequenceCreate(subject="Quick question", body="Hi {{firstName}}"))
client.campaigns.sequences.update("cmp_...", "seq_...", SequenceUpdate(delay_days=3))
client.campaigns.sequences.delete("cmp_...", "seq_...")
```

### Templates

```python
client.templates.list()
client.templates.get("tpl_...")
client.templates.create(TemplateCreate(name="Follow-up", body="Hi {{firstName}}", category="email"))
client.templates.update("tpl_...", TemplateUpdate(name="New name"))
client.templates.delete("tpl_...")
```

### Email Accounts

```python
client.email_accounts.list()
client.email_accounts.get("acc_...")
client.email_accounts.delete("acc_...")
```

### Inbox

```python
client.inbox.list_threads(category="interested", is_read=False)
client.inbox.get("rpl_...")                  # does not mark the thread read
client.inbox.get("rpl_...", mark_read=True)  # marks it read
client.inbox.update("rpl_...", ThreadUpdate(is_read=True))
```

### Analytics

```python
overview = client.analytics.overview()
print(f"Reply rate: {overview.reply_rate}%")

stats = client.analytics.campaign("cmp_...")
print(f"Sent: {stats.sent}, Replied: {stats.replied}")
```

## Error Handling

```python
from foxreach import FoxReach, NotFoundError, RateLimitError, AuthenticationError

client = FoxReach(api_key="otr_...")

try:
    lead = client.leads.get("cld_nonexistent")
except NotFoundError:
    print("Lead not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except AuthenticationError:
    print("Invalid API key")
```

## Configuration

```python
client = FoxReach(
    api_key="otr_...",
    base_url="https://api.foxreach.io/api/v1",  # default
    timeout=30.0,       # seconds
    max_retries=3,       # retries on 429
)
```

## Requirements

- Python 3.9+
- httpx
