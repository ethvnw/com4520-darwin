import csv
import datetime
import os

from fsm_gen.case_studies import *
from fsm_gen.mutator import Mutator
from walks.hsi import generate_harmonised_state_identifiers, generate_HSI_suite
from walks.random_walk import RandomWalk

FILENAME = (
    f"results/case_studies_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
)


def write_to_csv(
    case_study: FSMGenerator, percent: int, walk_type: RandomWalk.WalkType, result: dict
) -> None:
    """
    Write the results of the walk to a CSV file.
    Args:
        case_study (FSMGenerator): The FSM the walk was performed on.
        percent (int): The percentage of the FSM covered.
        walk_type (RandomWalk.WalkType): The type of walk performed.
        result (dict): The results of the walk.
    """
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                case_study,
                percent,
                result["hsi_len"],
                result["sum_hi"],
                walk_type,
                result["walk_len"],
                result["detected_fault_index"],
                result["time_taken"],
            ]
        )


def run_walk(
    case_study: FSMGenerator, percent: int, walk_type: RandomWalk.WalkType
) -> None:
    """
    Run a walk on the given case study and write the results to a CSV file.
    Args:
        case_study (FSMGenerator): The FSM to run the walk on.
        percent (int): The percentage of the FSM to cover.
        walk_type (RandomWalk.WalkType): The type of walk to perform.
    """
    len_state_identifiers = 0
    state_identifiers = generate_harmonised_state_identifiers(case_study)
    for set in state_identifiers.values():
        for seq in set:
            len_state_identifiers += len(seq)

    hsi_suite = generate_HSI_suite(case_study, state_identifiers)

    mutator = Mutator(case_study)
    mutated_fsm = mutator.create_mutated_fsm()

    walker = RandomWalk(case_study, mutated_fsm, percent, hsi_suite)

    start_time = datetime.datetime.now()
    walk = walker.walk(walk_type)
    end_time = datetime.datetime.now()
    detected_fault = walker.detected_fault(walk)

    results = {
        "sum_hi": len_state_identifiers,
        "hsi_len": len(hsi_suite),
        "walk_len": len(walk) if type(walk) == list else walk,
        "detected_fault_index": detected_fault,
        "time_taken": end_time - start_time,
    }

    write_to_csv(str(case_study), percent, walk_type, results)


def main():
    """
    Run in terminal:
    python3 case_study_experiments.py
    """
    percent_coverage = [80, 90, 95, 100]
    case_studies = [CoffeeMachine(), LocalisationSystem(), Phone()]

    if not os.path.exists("results"):
        os.mkdir("results")

    with open(FILENAME, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Case Study",
                "Percent Coverage",
                "HSI Suite Length",
                "Sum of HI",
                "Walk Type",
                "Walk Length",
                "Detected Fault Index",
                "Time Taken",
            ]
        )

    for case_study in case_studies:
        for _ in range(20):
            for walk_type in RandomWalk.WalkType:
                for percent in percent_coverage:
                    run_walk(case_study, percent, walk_type)


if __name__ == "__main__":
    main()
