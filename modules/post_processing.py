# modules/post_processing.py

import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def filter_detections(detection_results, confidence_threshold=0.5):
    """
    Filter detections based on confidence threshold.

    Args:
        detection_results (list): List of YOLO detection results for each frame.
        confidence_threshold (float): Minimum confidence score to retain a detection.

    Returns:
        list: List of filtered detections per frame.
    """
    filtered = []
    for idx, result in enumerate(detection_results):
        try:
            # Convert results to pandas DataFrame
            df = result.pandas().xyxy[0]

            # Apply confidence threshold
            df_filtered = df[df['confidence'] >= confidence_threshold]

            filtered.append(df_filtered)
            logging.info(f"Frame {idx + 1}: {len(df_filtered)} detections after filtering.")
        except Exception as e:
            logging.error(f"Error filtering detections for frame {idx + 1}: {e}")
            filtered.append(None)
    return filtered
