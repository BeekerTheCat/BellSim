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

    def __init__(self, vv: bool, pp: bool) -> None:
        self.vv = vv
        self.pp = pp

    def initialize_db(self, db: str, db_file: str) -> None:
        match db:
            case 'state':
                self._init_state_db(db_file)
            case 'trial':
                self._init_trial_db(db_file)
            case _:
                pass

    def _init_state_db(self, db_file: str):
        self.state = StateDB(db_file)

    def _init_trial_db(self, db_file: str):
        self.trial = TrialDB(db_file)


# EOF
