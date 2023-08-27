import time
from threading import Thread
from datetime import datetime, timedelta


def start_clean_up_task(simulations):
    thread = Thread(target=clean_up, args=(simulations,))
    thread.start()


def clean_up(simulations: dict):
    """Removes all simulations from the given input dictionary that are either
    started 3 days ago or finished 3 days ago.
    """
    while True:
        current_timestamp = datetime.now()
        simulations_to_remove = []
        for sim_uuid in simulations:
            sim = simulations[sim_uuid]
            if sim.timestamp_finished is None:
                if sim.timestamp_started + timedelta(days=3) < current_timestamp:
                    simulations_to_remove.append(sim_uuid)
            else:
                if sim.timestamp_finished + timedelta(days=3) < current_timestamp:
                    simulations_to_remove.append(sim_uuid)
        for sim_uuid in simulations_to_remove:
            simulations.pop(sim_uuid)
        time.sleep(1)
