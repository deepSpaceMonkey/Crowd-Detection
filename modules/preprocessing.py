# modules/preprocessing.py

import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def preprocess_frames(frames, target_size=(640, 640)):
    """
    Resize and normalize frames for YOLO model input.

    Args:
        frames (list): List of frames as numpy arrays.
        target_size (tuple): Desired size for YOLO input (width, height).

    Returns:
        list: List of preprocessed frames.
    """
    preprocessed = []
    for idx, frame in enumerate(frames):
        try:
            # Resize frame to target size required by YOLO
            resized_frame = cv2.resize(frame, target_size)

            # Normalize frame (scale pixel values to [0, 1])
            normalized_frame = resized_frame.astype(np.float32) / 255.0

            # Convert BGR to RGB because that's what deep learning modules like
            rgb_frame = cv2.cvtColor(normalized_frame, cv2.COLOR_BGR2RGB)

            preprocessed.append(rgb_frame)
        except Exception as e:
            logging.error(f"Error preprocessing frame {idx}: {e}")
    logging.info(f"Preprocessed {len(preprocessed)} frames.")
    return preprocessed
