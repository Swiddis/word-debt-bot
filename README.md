# Word Debt Bot

[![Continuous Integration](https://github.com/Swiddis/word-debt-bot/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/Swiddis/word-debt-bot/actions/workflows/continuous_integration.yml)
[![Coverage: codecov](https://codecov.io/gh/Swiddis/word-debt-bot/graph/badge.svg?token=E3AVRJUZ3V)](https://codecov.io/gh/Swiddis/word-debt-bot)
[![License: MIT](https://img.shields.io/badge/license-MIT-purple)](https://github.com/Swiddis/word-debt-bot/blob/main/LICENSE)
[![Versioning: semver](https://img.shields.io/badge/semver-1.0.2-blue)](https://semver.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Discord bot for running a little reading game among language learners.

## Usage

This project uses Poetry. Start by installing:

```sh
$ poetry install
...
Installing the current project: word_debt_bot (x.y.z)
```

Then you can run the project.
The `data` directory relative to the running location is used for storing state and logs.
A bot token needs to be provided in `data/TOKEN`.

```sh
$ poetry run python3 src/word_debt_bot/main.py
[Name] is ready.
```

You can also use Docker, and skip dealing with Poetry directly.
This still requires a `TOKEN` file, the local `./data` is used as a volume.

```sh
$ docker compose up --build
Attaching to word_debt_bot
```

## Development

For development, also install pre-commit:

```sh
$ poetry run pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

We use Pytest for testing:

```sh
$ poetry run pytest
...
=== N passed in Y.Zs ===
```

## Contributing

All contributions are welcome!
Please direct PRs to the `dev` branch, features will be bundled in a release with other contributions.
