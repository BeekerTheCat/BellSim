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

    @staticmethod
    def get_states_by_eo(entanglement_orientation: int) -> tuple[int, int]:
        p1 = ((2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 << entanglement_orientation) | (2348542582773833227889480594892199437311494003088532853857443830130122454711100468153595086332478834295701504 >> (360 - entanglement_orientation))) & ((1 << 360) - 1)
        p2 = ~p1 & ((1 << 360) - 1)
        return p1, p2

    @staticmethod
    def shift_state(state, shift) -> int:
        return ((state << shift) | (state >> (360 - shift))) & ((1 << 360) - 1)

    @staticmethod
    def measurement_angle_difference(p1_ma: int, p2_ma: int) -> int:
        diff = abs(p1_ma - p2_ma) % 360
        return min(diff, 360 - diff)

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

    def get_trial(self, eo: int, p1_ma: int, p2_ma: int):
        mad = self.measurement_angle_difference(p1_ma, p2_ma)
        mask = ((1 << 360) - 1)
        p1_es_int, p2_es_int = self.get_states_by_eo(eo)
        p1_ms_int = self.shift_state(p1_es_int, p1_ma)
        p2_ms_int = self.shift_state(p2_es_int, p2_ma)
        p1_es_int_z = ~p1_es_int & mask
        p2_es_int_z = ~p2_es_int & mask
        p1_ms_int_z = ~p1_ms_int & mask
        p2_ms_int_z = ~p2_ms_int & mask
        p1_es_p2_es_oo = p1_es_int & p2_es_int & mask
        p1_es_p2_es_zz = p1_es_int_z & p2_es_int_z & mask
        p1_es_p2_es_oz = p1_es_int & p2_es_int_z & mask
        p1_es_p2_es_zo = p1_es_int_z & p2_es_int & mask
        p1_ms_p2_ms_oo = p1_ms_int & p2_ms_int & mask
        p1_ms_p2_ms_zz = p1_ms_int_z & p2_ms_int_z & mask
        p1_ms_p2_ms_oz = p1_ms_int & p2_ms_int_z & mask
        p1_ms_p2_ms_zo = p1_ms_int_z & p2_ms_int & mask
        p1_es_p2_ms_oo = p1_es_int & p2_ms_int & mask
        p1_es_p2_ms_zz = p1_es_int_z & p2_ms_int_z & mask
        p1_es_p2_ms_oz = p1_es_int & p2_ms_int_z & mask
        p1_es_p2_ms_zo = p1_es_int_z & p2_ms_int & mask
        p1_ms_p2_es_oo = p1_ms_int & p2_es_int & mask
        p1_ms_p2_es_zz = p1_ms_int_z & p2_es_int_z & mask
        p1_ms_p2_es_oz = p1_ms_int & p2_es_int_z & mask
        p1_ms_p2_es_zo = p1_ms_int_z & p2_es_int & mask
        print(
            f"eo: {eo}\n"
            f"p1_ma: {p1_ma}\n"
            f"p2_ma: {p2_ma}\n"
            f"measurement angle difference: {mad}\n"
            f"p1_es: {p1_es_int:0360b}\n"
            f"p1_ms: {p1_ms_int:0360b}\n"
            f"p2_es: {p2_es_int:0360b}\n"
            f"p2_ms: {p2_ms_int:0360b}\n"
            f"bitwise p1 entanglement state vs p2 entanglement state\n"
            f"p1_es_p2_es_oo: {p1_es_p2_es_oo:0360b}\n"
            f"p1_es_p2_es_zz: {p1_es_p2_es_zz:0360b}\n"
            f"p1_es_p2_es_oz: {p1_es_p2_es_oz:0360b}\n"
            f"p1_es_p2_es_zo: {p1_es_p2_es_zo:0360b}\n"
            f"bitwise p1 measurement state vs p2 measurement state\n"
            f"p1_ms_p2_ms_oo: {p1_ms_p2_ms_oo:0360b}\n"
            f"p1_ms_p2_ms_zz: {p1_ms_p2_ms_zz:0360b}\n"
            f"p1_ms_p2_ms_oz: {p1_ms_p2_ms_oz:0360b}\n"
            f"p1_ms_p2_ms_zo: {p1_ms_p2_ms_zo:0360b}\n"
            f"bitwise p1 entanglement state vs p2 measurement state\n"
            f"p1_es_p2_ms_oo: {p1_es_p2_ms_oo:0360b}\n"
            f"p1_es_p2_ms_zz: {p1_es_p2_ms_zz:0360b}\n"
            f"p1_es_p2_ms_oz: {p1_es_p2_ms_oz:0360b}\n"
            f"p1_es_p2_ms_zo: {p1_es_p2_ms_zo:0360b}\n"
            f"bitwise p1 measurement state vs p2 entanglement state\n"
            f"p1_ms_p2_es_oo: {p1_ms_p2_es_oo:0360b}\n"
            f"p1_ms_p2_es_zz: {p1_ms_p2_es_zz:0360b}\n"
            f"p1_ms_p2_es_oz: {p1_ms_p2_es_oz:0360b}\n"
            f"p1_ms_p2_es_zo: {p1_ms_p2_es_zo:0360b}\n"
        )
        print(
            f"Entangled States\n"
            f"{p1_es_int:0360b}\n"
            f"{p2_es_int:0360b}\n"
            f"{p1_es_p2_es_oo:0360b}\n"
            f"{p1_es_p2_es_zz:0360b}\n"
            f"{p1_es_p2_es_oz:0360b}\n"
            f"{p1_es_p2_es_zo:0360b}\n"
            f"Measurement States\n"
            f"{p1_ms_int:0360b}\n"
            f"{p2_ms_int:0360b}\n"
            f"{p1_ms_p2_ms_oo:0360b}\n"
            f"{p1_ms_p2_ms_zz:0360b}\n"
            f"{p1_ms_p2_ms_oz:0360b}\n"
            f"{p1_ms_p2_ms_zo:0360b}\n"
            f"P1 Entangled State & P2 Measurement State\n"
            f"{p1_es_int:0360b}\n"
            f"{p2_ms_int:0360b}\n"
            f"{p1_es_p2_ms_oo:0360b}\n"
            f"{p1_es_p2_ms_zz:0360b}\n"
            f"{p1_es_p2_ms_oz:0360b}\n"
            f"{p1_es_p2_ms_zo:0360b}\n"
            f"P1 Measurement State & P2 Entangled State\n"
            f"{p1_ms_int:0360b}\n"
            f"{p2_es_int:0360b}\n"
            f"{p1_ms_p2_es_oo:0360b}\n"
            f"{p1_ms_p2_es_zz:0360b}\n"
            f"{p1_ms_p2_es_oz:0360b}\n"
            f"{p1_ms_p2_es_zo:0360b}\n"
        )
        print(f"Trial ({eo:3}, {p1_ma:3}, {p2_ma:3}, {mad:3})")


# EOF
