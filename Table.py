# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS


# PARAMETERS
# FUNCTIONS
# CLASSES
class DBTable:
    name: str

    def __init__(self, name: str):
        self.name = name


class AngleTB(DBTable):
    def __init__(self, name: str):
        super().__init__(name)


class PhotonTB(DBTable):
    def __init__(self, name: str):
        super().__init__(name)


class BitwiseTB(PhotonTB):
    def __init__(self, name: str):
        super().__init__(name)


# EOF
