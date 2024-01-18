# Word Debt Bot

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

You can also use Docker, and skip dealing with Poetry directly:

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
