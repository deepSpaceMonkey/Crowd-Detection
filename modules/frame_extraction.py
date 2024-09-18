# modules/frame_extraction.py

from pathlib import Path
import cv2
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def extract_specific_frames(video_path, timestamps):
    """
    Extracts frames from a video at specified timestamps.

    Parameters:
        video_path (Path or str): Path to the processed video file.
        timestamps (list of float): List of timestamps (in seconds) at which to extract frames.

    Returns:
        dict: A dictionary mapping each timestamp to its corresponding frame as a NumPy array.
    """
    video_path = Path(video_path)  # Ensure video_path is a Path object

    if not video_path.exists():
        logging.error(f"Video file {video_path} not found.")
        return {}

    vidcap = cv2.VideoCapture(str(video_path))
    if not vidcap.isOpened():
        logging.error(f"Cannot open video file {video_path}.")
        return {}

    original_fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = total_frames / original_fps if original_fps > 0 else 0

    if original_fps <= 0:
        logging.error("Invalid frame rate detected.")
        vidcap.release()
        return {}

    logging.info(f"Video FPS: {original_fps}")
    logging.info(f"Total Frames: {total_frames}")
    logging.info(f"Video Duration: {duration:.2f} seconds")

    frames = {}
    for timestamp in timestamps:
        if timestamp < 0 or timestamp > duration:
            logging.warning(f"Timestamp {timestamp}s is out of video duration range.")
            continue

        frame_number = int(timestamp * original_fps)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = vidcap.read()
        if success:
            frames[timestamp] = frame
            logging.info(f"Extracted frame at {timestamp}s (Frame {frame_number}).")
        else:
            logging.error(f"Failed to extract frame at {timestamp}s.")

    vidcap.release()
    return frames
