# enum for role
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"
    teacher = "teacher"