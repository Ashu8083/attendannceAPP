"""
Seeder package for generating initial system data, permissions, default roles, and model seeders.
"""

from app.seeder.main_seeder import seed_database
from app.seeder.employee_face_seeder import seed_attendance

__all__ = ["seed_database", "seed_attendance"]
