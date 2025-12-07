# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-06

### Added
- Initial release of agentape
- Record/replay functionality for LLM agents
- OpenAI client wrapper with automatic interaction recording
- `@record` context manager for capturing LLM interactions to tape files
- `@replay` context manager for replaying interactions without API calls
- YAML-based tape storage format
- Exact request matching for deterministic replay
- Pytest integration with `@use_tape` decorator
- Pytest plugin with `--tape-mode` CLI option (record/replay/off)
- Support for streaming responses
- Comprehensive test suite with 39 passing tests
- MIT License

### Supported
- Python 3.10+
- OpenAI SDK (v1.0.0+)
- YAML tape format

### Documentation
- README with quick start guide
- Installation instructions
- Pytest integration examples
- Publishing guide for maintainers

[0.1.0]: https://github.com/agentape/agentape/releases/tag/v0.1.0
