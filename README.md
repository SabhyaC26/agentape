# agentape

Record/replay testing for LLM agents.

## Installation

```bash
pip install agentape
```

## Quick Start

```python
import agentape
from openai import OpenAI

# Wrap the client
client = agentape.wrap(OpenAI())

# Record interactions
with agentape.record("tapes/my_flow.yaml"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )

# Replay interactions (no API calls made)
with agentape.replay("tapes/my_flow.yaml"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
```

## pytest Integration

```python
import agentape

@agentape.use_tape("tapes/{test_name}.yaml")
def test_my_feature(openai_client):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
    assert "hello" in response.choices[0].message.content.lower()
```

Run tests with:

```bash
pytest tests/ --tape-mode=record   # Record new tapes
pytest tests/ --tape-mode=replay   # Replay existing (default)
pytest tests/ --tape-mode=off      # Pass-through, no taping
```

## License

MIT