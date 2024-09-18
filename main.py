import logging
from pathlib import Path
from modules.video_preperation import prepare_video
from modules.frame_extraction import extract_specific_frames

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def process_video():
    # Define the video processing parameters
    input_filename = "resources/droneFootageCrowd_full.mp4"
    trimmed_filename = "resources/droneFootage_trimmed.mp4"
    start_time = "00:00:14"
    end_time = "00:00:32"

    # Define the paths
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_filename
    trimmed_path = script_dir / trimmed_filename

    # Trim the video
    logging.info("Starting video trimming...")
    success = prepare_video(input_filename, str(trimmed_path), start_time, end_time)

    if success:
        logging.info(f"Video has been successfully trimmed and saved to {trimmed_path}.")
    else:
        logging.error("There was an issue processing the video.")
        return  # Exit if video processing failed

    # Define the timestamps for frame extraction
    timestamps = [0, 13]  # Start and 13 seconds

    # Extract frames
    logging.info("Starting frame extraction...")
    frames = extract_specific_frames(str(trimmed_path), timestamps)


if __name__ == "__main__":
    process_video()
    logging.info("Done.")
