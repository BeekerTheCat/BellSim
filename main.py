# STANDARD IMPORTS
from __future__ import annotations
# CUSTOM IMPORTS
from Simulation import BellSim


# PARAMETERS
STATE_LOOKUP_DATABASE = "states.db"
TRIAL_LOOKUP_DATABASE = "trials.db"
VERBOSE = True
PAUSE_PROMPT = True


# FUNCTIONS
# CLASSES


# MAIN
def main(state_db: str, trial_db: str, verbose: bool, pause_prompt: bool):
    sim = BellSim(vv=verbose, pp=pause_prompt)
    sim.initialize_db('state', state_db)
    if sim.state.angle.row_count < 360:
        sim.state.populate("angle")
    sim.initialize_db('trial', trial_db)


# RUN
if __name__ == "__main__":
    parameters = [
        STATE_LOOKUP_DATABASE,
        TRIAL_LOOKUP_DATABASE,
        VERBOSE,
        PAUSE_PROMPT
    ]
    main(*parameters)


# EOF
