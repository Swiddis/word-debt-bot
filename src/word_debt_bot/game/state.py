from dataclasses import dataclass

from word_debt_bot.game.player import WordDebtPlayer


@dataclass
class WordDebtState:
    """Tracker for most recent word debt states, used for type checking."""

    version: int
    users: dict[str, WordDebtPlayer | dict]
    modifiers: list[dict[str, str | float]]  # TODO fully specify modifier type

    def __post_init__(self):
        if isinstance(self.users, dict):
            self.users = {
                key: WordDebtPlayer(**value) for key, value in self.users.items()
            }
