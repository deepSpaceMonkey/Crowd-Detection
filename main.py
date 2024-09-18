# main.py

import logging
from pathlib import Path
from modules.video_preparation import prepare_video
from modules.frame_extraction import extract_specific_frames
from modules.preprocessing import preprocess_frames
from modules.yolo_model import YOLODetector
from modules.post_processing import filter_detections
from modules.counting import count_people, aggregate_counts

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def process_video():
    # Step 1: Video Preparation (Trim and Remove Audio)
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
    success = prepare_video(str(input_path), str(trimmed_path), start_time, end_time)

    if success:
        logging.info(f"Video has been successfully trimmed and saved to {trimmed_path}.")
    else:
        logging.error("There was an issue processing the video.")
        return  # Exit if video processing failed

    # Step 2: Frame Extraction
    # Define the timestamps for frame extraction
    timestamps = [0, 13]  # Start and 13 seconds

    logging.info("Starting frame extraction...")
    frames_dict = extract_specific_frames(str(trimmed_path), timestamps)

    if not frames_dict:
        logging.error("No frames extracted. Exiting.")
        return

    # Convert frames dict to list for further processing
    frames = list(frames_dict.values())

    # Step 3: Preprocessing
    logging.info("Starting frame preprocessing...")
    preprocessed_frames = preprocess_frames(frames)

    if not preprocessed_frames:
        logging.error("Frame preprocessing failed. Exiting.")
        return

    # Step 4: YOLOv8 Model Setup
    yolo_model_name = 'yolov8s.pt'
    logging.info("Initializing YOLOv8 model...")
    try:
        yolo_detector = YOLODetector(model_name=yolo_model_name)
    except Exception:
        logging.error("YOLO model setup failed. Exiting.")
        return

    # Step 5: Object Detection
    logging.info("Starting object detection...")
    detections = yolo_detector.detect(preprocessed_frames)

    if not detections:
        logging.error("Object detection failed. Exiting.")
        return

    # Step 6: Post-Processing
    confidence_threshold = 0.5  # Adjust based on your requirements
    logging.info("Starting post-processing of detections...")
    filtered_detections = filter_detections(detections, confidence_threshold=confidence_threshold)

    if not filtered_detections:
        logging.error("Post-processing failed. Exiting.")
        return

    # Step 7: Counting
    logging.info("Counting detected people...")
    counts = count_people(filtered_detections)
    estimated_crowd_size = aggregate_counts(counts)

    logging.info(f"Final Estimated Crowd Size: {estimated_crowd_size}")


if __name__ == "__main__":
    process_video()
    logging.info("Done.")
