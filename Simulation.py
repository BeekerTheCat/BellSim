# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS
from Database import StateDB, TrialDB


# PARAMETERS
# FUNCTIONS
# CLASSES
class BellSim:
    vv: bool
    pp: bool
    state: StateDB
    trial: TrialDB

    def __init__(self, vv: bool, pp: bool):
        self.vv = vv
        self.pp = pp

    def initialize_db(self, db: str, db_file: str):
        match db:
            case 'state':
                self.state = StateDB(name=db_file)
            case 'trial':
                self.trial = TrialDB(name=db_file)
            case _:
                pass


# EOF
