# Word Debt Bot

[![Continuous Integration](https://github.com/Swiddis/word-debt-bot/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/Swiddis/word-debt-bot/actions/workflows/continuous_integration.yml)
[![Coverage: codecov](https://codecov.io/gh/Swiddis/word-debt-bot/graph/badge.svg?token=E3AVRJUZ3V)](https://codecov.io/gh/Swiddis/word-debt-bot)
[![License: MIT](https://img.shields.io/badge/license-MIT-purple)](LICENSE)
[![Versioning: semver](https://img.shields.io/badge/semver-1.1.1-blue)](https://semver.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A Discord bot for running a game between friends, to motivate us to read more.

What started as accountability, and turned into a competition:
Word Debt is a game to encourage reading.
For every 1000 words you read, you gain Cranes, which can be spent on... Two items. (We're working on it!)
Each player also has an amount of word debt that they clear by reading those words away.
The project is still in its infancy, so there are lots of open issues,
as well as multiple design points still open for discussion.

## Installation

First you need to [create a Discord app](https://discord.com/developers/docs/getting-started) to run the bot.
The bot's token needs to be stored in the `data` directory in a file named `TOKEN`.

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Begin by installing the project:

```sh
$ poetry install
...
Installing the current project: word_debt_bot (x.y.z)
```

Run the project from the same directory that the `data` directory is in, typically the project root.
The `data` directory is used for storing state and logs.

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

## Contributing

We welcome community contributions, beginners welcome!
See especially issues labeled `help wanted` or `good first issue` for starting points, or `discussion` to share thoughts on game design.
Questions on how to approach a feature are well-received.

Please direct PRs to the `dev` branch, features will be bundled in a release with other contributions.

For development, also install pre-commit,
which will automatically apply lints to avoid formatting issues with CI checks:

```sh
$ poetry run pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Testing for new functionality is expected.
We use Pytest for testing:

```sh
$ poetry run pytest
...
=== N passed in Y.Zs ===
```

Optionally pass `--cov=src` for a coverage report.

## License

[MIT License](LICENSE)
