# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS
from Database import StateDB, TrialDB


# PARAMETERS
# FUNCTIONS
def circular_shift_left(shift):
    return ((2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 << shift) | (2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 >> (360 - shift))) & ((1 << 360) - 1)


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

    @staticmethod
    def get_states_by_eo(entanglement_orientation: int) -> tuple[int, int]:
        p1 = ((2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 << entanglement_orientation) | (2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 >> (360 - entanglement_orientation))) & ((1 << 360) - 1)
        p2 = ~p1 & ((1 << 360) - 1)
        return p1, p2

    @staticmethod
    def shift_state(state, shift) -> int:
        return ((state << shift) | (state >> (360 - shift))) & ((1 << 360) - 1)

    def run(self, entanglement_orientations: int = 360, measurement_angles: int = 360):
        for eo in range(entanglement_orientations):
            p1_es_int, p2_es_int = self.get_states_by_eo(eo)
            for p1_ma in range(measurement_angles):
                p1_ms_int = self.shift_state(p1_es_int, p1_ma)
                for p2_ma in range(measurement_angles):
                    p2_ms_int = self.shift_state(p2_es_int, p2_ma)
                    print(
                        f"eo: {eo}\n"
                        f"p1_ma: {p1_ma}\n"
                        f"p2_ma: {p2_ma}\n"
                        f"p1_es: {p1_es_int:0360b}\n"
                        f"p1_ms: {p1_ms_int:0360b}\n"
                        f"p2_es: {p2_es_int:0360b}\n"
                        f"p2_ms: {p2_ms_int:0360b}\n"
                    )
                    input(f"Trial ({eo:3}, {p1_ma:3}, {p2_ma:3}) Press any key to continue...")


# EOF
