#commands
from enum import Enum


class Command(Enum):
    ATTACK = 1
    THROW = 2
    BLOCK = 3
    JUMP = 4
    HORIZONTAL_MOVEMENT = 5
    HORIZONTAL_AIM = 6
    VERTICAL_AIM = 7