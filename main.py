import logging
from pathlib import Path
from video_preperation import prepare_video

# Configure logging for the main script
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def test_video_prep():
    # Define the test parameters
    input_filename = "droneFootageCrowd_full.mp4"
    output_filename = "droneFootage_trimmed.mp4"
    start_time = "00:00:14"
    end_time = "00:00:32"

    # Define the output path
    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / output_filename

    success = prepare_video(input_filename, str(output_path), start_time, end_time)

    # Check if the process was successful and log the appropriate message
    if success:
        logging.info(f"Video has been successfully trimmed and saved to {output_path}.")
    else:
        logging.error("There was an issue processing the video.")


if __name__ == "__main__":
    test_video_prep()
