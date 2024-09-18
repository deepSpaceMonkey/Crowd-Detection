from pathlib import Path
import subprocess
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def prepare_video(input_filename, output_path, start_time, end_time):
    """
    Trims the input video to a specified segment and removes the audio.

    Parameters:
        input_filename (str): Filename of the original video file located in the parent directory.
        output_path (str): Path to save the processed video.
        start_time (str): Start time for trimming (e.g., "00:00:14").
        end_time (str): End time for trimming (e.g., "00:00:32").

    Returns:
        bool: True if processing is successful, False otherwise.
    """
    # Determine the directory where the script is located
    script_dir = Path(__file__).resolve().parent

    # Construct the path to the input video in the current directory
    input_path = (script_dir / input_filename).resolve()

    if not input_path.exists():
        logging.error(f"Input file {input_path} does not exist.")
        return False

    logging.info("Starting video trimming and audio removal...")

    command = [
        'ffmpeg',
        '-i', input_path,
        '-ss', start_time,
        '-to', end_time,
        '-an',  # Remove audio
        '-c', 'copy',
        output_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        logging.info("Video processing completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Video processing failed.")
        return False
