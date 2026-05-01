# Grumpy Python SDK

Zero-config AI SRE teammate that aggressively complains about your crashes.

## Installation

```bash
pip install desicon-grumpy
```

## Usage

Initialize the client as early as possible in your application (e.g., at the top of your `main.py` or `manage.py`).

```python
from grumpy_ai import GrumpyClient

GrumpyClient(
    api_key="grp_live_...",
    app_name="fastapi-backend",
    environment="production"
)

# That's it! Grumpy automatically hooks into sys.excepthook.
# Any unhandled exception will be intercepted, analyzed by AI, and sent to your Discord/Slack.
```
