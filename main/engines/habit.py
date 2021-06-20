"""Module for habit-related operations"""
from typing import Optional, List
from main.models.habit import Habit
from main.enums import HabitStatus


def get_habit(habit_id: int) -> Optional[Habit]:
    """Return a habit by id or None if habit not found"""
    return Habit.find_by_id(habit_id)


def update_habit(habit: Habit, data: dict) -> Habit:
    """Update a habit by id"""
    Habit.update_by_id(habit.id, data)
    return Habit.find_by_id(habit.id)


def create_habit(*, user_id: int, name: str, countable: Optional[bool] = None) -> Habit:
    """Create and save a habit into database, then return the habit"""
    habit = Habit(user_id=user_id, name=name, countable=countable)
    habit.save()
    return habit


def query_habits_by_user_id(user_id: int):
    """Return a habits query object after filtering habits by user_id and status='active'"""
    return Habit.query.filter_by(user_id=user_id, status=HabitStatus.ACTIVE)


def get_habit_count(user_id: int) -> int:
    """Return count of all habits owned by user"""
    return query_habits_by_user_id(user_id).count()


def get_habits_paginated(
    user_id: int, page: int, habits_per_page: int, show_errors: bool
) -> List[Habit]:
    """Return a paginated list of habits"""
    habits = (
        query_habits_by_user_id(user_id)
        .order_by(Habit.created_at.desc())
        .paginate(page, habits_per_page, show_errors)
        .items
    )
    return habits
