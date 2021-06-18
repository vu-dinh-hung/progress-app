"""Module for HabitEngine"""
from main.models.habit import Habit
from main.enums import HabitStatus


class HabitEngine:
    """Engine class for providing habit-related operations"""

    @staticmethod
    def find_by_id(*args, **kwargs):
        """Return a habit by id or None if habit not found"""
        return Habit.find_by_id(*args, **kwargs)

    @staticmethod
    def update_by_id(*args, **kwargs):
        """Update a habit by id"""
        Habit.update_by_id(*args, **kwargs)

    @staticmethod
    def create_habit(*args, **kwargs):
        """Create and save a habit into database, then return the habit"""
        habit = Habit(*args, **kwargs)
        habit.save()
        return habit

    @staticmethod
    def query_habits_by_user_id(user_id):
        """Return a habits query object after filtering habits by user_id and status='active'"""
        return Habit.query.filter_by(user_id=user_id, status=HabitStatus.ACTIVE)

    @classmethod
    def get_habit_count(cls, user_id):
        """Return count of all habits owned by user"""
        return cls.query_habits_by_user_id(user_id).count()

    @classmethod
    def get_habits_paginated(cls, user_id, *args):
        """Return a paginated list of habits"""
        habits = (
            cls.query_habits_by_user_id(user_id)
            .order_by(Habit.created_at.desc())
            .paginate(*args)
            .items
        )
        return habits
