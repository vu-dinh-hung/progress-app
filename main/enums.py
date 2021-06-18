"""Module for app enums"""
from enum import Enum


class HabitStatus(Enum):
    """Enum class for Habit-specific statuses"""

    ACTIVE = "active"
    DELETED = "deleted"


class LogStatus(Enum):
    """Enum class for Log-specific statuses"""

    ACTIVE = "active"
    DELETED = "deleted"
