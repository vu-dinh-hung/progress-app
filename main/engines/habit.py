"""Module for habit-related operations"""
from main.models.habit import Habit
from main.enums import HabitStatus


def get_habit(habit_id):
    """Return a habit by id or None if habit not found"""
    return Habit.find_by_id(habit_id)


def update_habit(habit_id, data):
    """Update a habit by id"""
    Habit.update_by_id(habit_id, data)


def create_habit(*args, **kwargs):
    """Create and save a habit into database, then return the habit"""
    habit = Habit(*args, **kwargs)
    habit.save()
    return habit


def query_habits_by_user_id(user_id):
    """Return a habits query object after filtering habits by user_id and status='active'"""
    return Habit.query.filter_by(user_id=user_id, status=HabitStatus.ACTIVE)


def get_habit_count(user_id):
    """Return count of all habits owned by user"""
    return query_habits_by_user_id(user_id).count()


def get_habits_paginated(user_id, *args):
    """Return a paginated list of habits"""
    habits = (
        query_habits_by_user_id(user_id)
        .order_by(Habit.created_at.desc())
        .paginate(*args)
        .items
    )
    return habits
