# modules/yolo_model.py

from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class YOLODetector:
    def __init__(self, model_name='yolov8s.pt', device='cuda' if torch.cuda.is_available() else 'cpu'):
        """
        Initialize the YOLOv8 model.

        Args:
            model_name (str): Name of the YOLOv8 model to load.
            device (str): Device to run the model on.
        """
        self.device = device
        try:
            # Initialize the YOLOv8 model
            self.model = YOLO(model_name)
            self.model.to(self.device)
            logging.info(f"YOLOv8 model '{model_name}' loaded successfully on {self.device}.")
        except Exception as e:
            logging.error(f"Failed to load YOLOv8 model '{model_name}': {e}")
            raise e

    def detect(self, frames):
        """
        Perform object detection on preprocessed frames.

        Args:
            frames (list): List of preprocessed frames as numpy arrays.

        Returns:
            list: List of detection results for each frame.
        """
        detections = []
        try:
            for idx, frame in enumerate(frames):
                # Perform detection
                result = self.model(frame)
                detections.append(result)
                logging.info(f"Performed detection on frame {idx + 1}/{len(frames)}.")
        except Exception as e:
            logging.error(f"Error during detection: {e}")
        return detections
