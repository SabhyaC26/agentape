#!/usr/bin/env python3
"""Example demonstrating agentape record/replay functionality."""

import os

from dotenv import load_dotenv
from openai import OpenAI

import agentape

# Load environment variables from .env file
load_dotenv()

# Note: This example requires an OPENROUTER_API_KEY in your .env file


def demo_basic_usage():
    """Demonstrate basic record and replay."""
    print("=" * 60)
    print("AgentTape Example: Basic Record/Replay")
    print("=" * 60)

    # Step 1: Wrap the OpenAI client configured for OpenRouter
    client = agentape.wrap(
        OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
    )
    print("\n✓ Wrapped OpenAI client with OpenRouter")

    # Step 2: Record an interaction
    print("\n[RECORD MODE] Making API call and recording to tape...")
    with agentape.record("tapes/example.yaml"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": "Say 'Hello from agentape!'"}],
        )
        recorded_content = response.choices[0].message.content
        print(f"Response: {recorded_content}")

    print("✓ Saved to tapes/example.yaml")

    # Step 3: Replay the interaction (no API call made!)
    print("\n[REPLAY MODE] Loading cached response from tape...")
    with agentape.replay("tapes/example.yaml"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": "Say 'Hello from agentape!'"}],
        )
        replayed_content = response.choices[0].message.content
        print(f"Response: {replayed_content}")

    print("✓ No API call made - response came from tape!")

    # Verify they match
    assert recorded_content == replayed_content, (
        "Recorded and replayed responses should match"
    )
    print("\n✓ Recorded and replayed responses match perfectly\n")


def demo_streaming():
    """Demonstrate streaming support."""
    print("=" * 60)
    print("AgentTape Example: Streaming Support")
    print("=" * 60)

    client = agentape.wrap(
        OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
    )

    # Record streaming
    print("\n[RECORD MODE] Streaming API call...")
    with agentape.record("tapes/streaming_example.yaml"):
        stream = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": "Count to 5"}],
            stream=True,
        )
        print("Response: ", end="", flush=True)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()

    print("✓ Streaming response saved to tape")

    # Replay streaming
    print("\n[REPLAY MODE] Replaying streamed response...")
    with agentape.replay("tapes/streaming_example.yaml"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Count to 5"}],
            stream=True,
        )
        print("Response: ", end="", flush=True)
        for chunk in stream:
            if chunk.get("choices", [{}])[0].get("delta", {}).get("content"):
                print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
        print()

    print("✓ Streamed response replayed from tape\n")


if __name__ == "__main__":
    try:
        demo_basic_usage()
        print("\n" + "=" * 60 + "\n")
        demo_streaming()

        print("\nAll examples completed successfully!")
        print("\nCheck the 'tapes/' directory to see the recorded YAML files.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(
            "\nMake sure OPENROUTER_API_KEY is set in your environment for record mode."
        )
        print("Or use replay mode with existing tapes.")
