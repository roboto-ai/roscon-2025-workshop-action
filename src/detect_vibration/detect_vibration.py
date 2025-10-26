import pandas
import roboto


def create_vibration_events_for_topic(df: pandas.DataFrame, tp: roboto.Topic):
    # Find contiguous windows where vibration > 9.8 m/s²
    high_vib = df["accel_vibration_metric"] > 9.8
    changes = high_vib.ne(high_vib.shift()).cumsum()

    for _, group in df[high_vib].groupby(changes[high_vib]):
        start_time = int(group.index[0])
        end_time = int(group.index[-1])

        if start_time == end_time:
            continue

        mean_vibration = group["accel_vibration_metric"].mean()
        max_vibration = group["accel_vibration_metric"].max()

        roboto.Event.create(
            start_time=start_time,
            end_time=end_time,
            name="high_vibration",
            description=(
                "Warning: Vibration levels are critically high (above 9.81 m/s²). "
                f"The measured mean vibration was {mean_vibration:.2f} m/s² "
                f"with a max of {max_vibration:.2f} m/s². "
                "Further investigation is recommended to avoid potential damage or performance "
                "degradation. Excessive vibration can severely impact flight stability and "
                "sensor accuracy."
            ),
            message_path_ids=[tp.get_message_path("accel_vibration_metric").message_path_id],
            display_options=roboto.EventDisplayOptions(color="red"),
            caller_org_id=tp.org_id,
        )