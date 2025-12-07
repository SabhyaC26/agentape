<p align="center">
  <img src="agentapelogo.png" alt="agentape logo" width="300" style="border-radius: 20px">
</p>

<p align="center">
    <a href="https://pypi.org/project/agentape/">
        <img src="https://img.shields.io/pypi/v/agentape.svg" alt="PyPI version">
    </a>
    <a href="https://pypi.org/project/agentape/">
        <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python versions">
    </a>
    <a href="LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    </a>
</p>

<p align="center">
  <b>Record/replay testing for LLM agents.</b>
</p>

## Why Agentape?

Depending on live LLM APIs for testing is slow, expensive, and flaky. **Agentape** solves this by recording your interactions once and replaying them instantly.

- 💸 **Save Money**: Eliminate API costs during development and CI/CD.
- ⚡ **Instant Feedback**: Tests run in milliseconds, not seconds.
- 🛡️ **Determinism**: Flaky LLM outputs won't break your logic tests.
- 🔒 **Offline Capable**: Code on a plane or train without internet access.

## Use Cases

- **Regression Testing**: Ensure your tool usage and parsing logic works without hitting real endpoints.
- **CI/CD Pipelines**: Run unittests on every commit without worrying about rate limits or bills.
- **Showcase Demos**: commit "golden path" tapes to ensure your examples always work for new users.
- **Debugging**: Capture a specific conversation state and replay it reliably to fix downstream bugs.

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