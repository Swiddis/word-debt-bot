from dataclasses import dataclass

from beartype import beartype


@dataclass
class WordDebtPlayer:
    """Class for tracking player information."""

    user_id: str
    display_name: str
    word_debt: int = 0
    crane_payment_rollover: int = 0
    cranes: int = 0
