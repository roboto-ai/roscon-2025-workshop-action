import roboto

from .detect_vibration import create_vibration_events_for_topic
from .logger import logger


def main(context: roboto.InvocationContext) -> None:
    logger.setLevel(context.log_level)

    action_input = context.get_input()

    if action_input.files:
        logger.info("Processing %d input file(s):", len(action_input.files))
        for file, local_path in action_input.files:
            tp = file.get_topic("vehicle_imu_status_00")
            df = tp.get_data_as_df(["accel_vibration_metric"])

            create_vibration_events_for_topic(df, tp)

    else:
        logger.info("No input files provided")
