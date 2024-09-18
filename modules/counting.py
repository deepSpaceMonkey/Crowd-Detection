# modules/counting.py

import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def count_people(filtered_detections, target_class='person'):
    """
    Count the number of people detected in each frame.

    Args:
        filtered_detections (list): List of filtered detections per frame.
        target_class (str): The class label to count (default is 'person').

    Returns:
        list: List of counts per frame.
    """
    counts = []
    for idx, df in enumerate(filtered_detections):
        try:
            if df is not None:
                count = df[df['name'] == target_class].shape[0]
            else:
                count = 0
            counts.append(count)
            logging.info(f"Frame {idx + 1}: {count} {target_class}(s) detected.")
        except Exception as e:
            logging.error(f"Error counting people in frame {idx + 1}: {e}")
            counts.append(0)
    return counts


def aggregate_counts(counts):
    """
    Aggregate counts across all frames to estimate total crowd size.

    Args:
        counts (list): List of counts per frame.

    Returns:
        int: Estimated total crowd size.
    """
    if not counts:
        logging.warning("No counts available to aggregate.")
        return 0
    average_count = sum(counts) / len(counts)
    estimated_crowd_size = int(average_count)
    logging.info(f"Estimated Crowd Size: {estimated_crowd_size}")
    return estimated_crowd_size
