"""Factory for building split strategy instances."""

from typing import Dict
from enum import Enum
from ..entities.user import User
from .base import SplitStrategy
from .equal import EqualSplitStrategy
from .percentage import PercentageSplitStrategy
from .custom import CustomSplitStrategy


class SplitType(Enum):
    """Allowed split type identifiers."""
    EQUAL = "equal"
    PERCENTAGE = "percentage"
    CUSTOM = "custom"


class SplitStrategyFactory:
    """Create split strategies based on input type."""

    @staticmethod
    def create(
        split_type: SplitType,
        data: Dict[User, float] | None = None
    ) -> SplitStrategy:
        """Return the appropriate split strategy instance."""

        if split_type == SplitType.EQUAL:
            return EqualSplitStrategy()

        if split_type == SplitType.PERCENTAGE:
            if not data:
                raise ValueError("Percentage data required")
            return PercentageSplitStrategy(data)

        if split_type == SplitType.CUSTOM:
            if not data:
                raise ValueError("Custom split data required")
            return CustomSplitStrategy(data)

        raise ValueError(f"Unsupported split type: {split_type}")
