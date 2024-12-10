# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS
from Table import AngleTB, PhotonTB, BitwiseTB


# PARAMETERS
# FUNCTIONS
# CLASSES
class Database:
    name: str

    def __init__(self, name: str):
        self.name = name


class StateDB(Database):
    pass


class TrialDB(Database):
    pass


# EOF
