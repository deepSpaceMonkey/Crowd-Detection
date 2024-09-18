# tests/test_extract_frames.py

import unittest
from pathlib import Path
import cv2
import logging

# Import the functions to be tested
from video_preperation import prepare_video
from frame_extraction import extract_specific_frames

# Configure logging for the tests
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class TestExtractFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up test environment before any tests are run.
        This includes trimming the video to ensure it's ready for frame extraction.
        """
        # Define project directories and filenames
        cls.script_dir = Path(__file__).resolve().parent.parent  # Assuming tests/ is inside the project directory
        cls.input_filename = "droneFootageCrowd_full.mp4"
        cls.trimmed_filename = "droneFootage_trimmed_test_extract.mp4"
        cls.trimmed_path = cls.script_dir / cls.trimmed_filename
        cls.frames_dir = cls.script_dir / "frames"

        # Create frames directory if it doesn't exist
        cls.frames_dir.mkdir(exist_ok=True)

        # Trim the video for frame extraction
        start_time = "00:00:00"   # Start trimming at the beginning
        end_time = "00:00:18"     # End trimming at 18 seconds

        logging.info("Starting video trimming for frame extraction tests...")
        success = prepare_video(
            input_filename=cls.input_filename,
            output_path=str(cls.trimmed_path),
            start_time=start_time,
            end_time=end_time
        )

        # Assert that the video preparation was successful
        if not success:
            raise unittest.SkipTest("Video trimming failed, skipping frame extraction tests.")

        # Assert that the trimmed video exists
        if not cls.trimmed_path.exists():
            raise unittest.SkipTest("Trimmed video file does not exist, skipping frame extraction tests.")

        # Optionally, check the duration of the trimmed video
        vidcap = cv2.VideoCapture(str(cls.trimmed_path))
        if vidcap.isOpened():
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = total_frames / fps if fps > 0 else 0
            vidcap.release()

            expected_duration = 18  # From 0s to 18s
            # With the following lines:
            if abs(duration - expected_duration) > 0.5:
                cls.fail(f"Trimmed video duration {duration}s is not approximately {expected_duration}s.")
            logging.info(f"Trimmed video duration verified: {duration:.2f} seconds.")
        else:
            raise unittest.SkipTest("Failed to open the trimmed video for duration check in frame extraction tests.")

    def test_extract_specific_frames(self):
        """
        Test the extract_specific_frames function to ensure it extracts the correct frames.
        """
        # Define the timestamps for frame extraction
        timestamps = [0, 13]  # Start and 13 seconds

        # Extract frames
        logging.info("Starting frame extraction...")
        frames = extract_specific_frames(str(self.trimmed_path), timestamps)

        # Assert that frames were extracted
        self.assertEqual(len(frames), len(timestamps),
                         "Number of extracted frames does not match the number of timestamps.")

        # Save the frames to the frames directory for manual verification
        for timestamp, frame in frames.items():
            frame_filename = f"frame_{int(timestamp)}s_test.jpg"
            frame_path = self.frames_dir / frame_filename
            success = cv2.imwrite(str(frame_path), frame)
            self.assertTrue(success, f"Failed to write frame at {timestamp}s to {frame_path}.")

            logging.info(f"Saved frame at {timestamp}s to {frame_path}.")

        # Optionally, verify that the saved frames exist
        for timestamp in timestamps:
            frame_filename = f"frame_{int(timestamp)}s_test.jpg"
            frame_path = self.frames_dir / frame_filename
            self.assertTrue(frame_path.exists(), f"Frame file {frame_path} does not exist.")

    @classmethod
    def tearDownClass(cls):
        """
        Uncomment to clean up after all tests are run.
        """
        # if cls.trimmed_path.exists():
        #     cls.trimmed_path.unlink()
        #
        # for frame_file in cls.frames_dir.iterdir():
        #     if frame_file.is_file():
        #         frame_file.unlink()
        #
        # cls.frames_dir.rmdir()

        pass  # Currently, do nothing


if __name__ == '__main__':
    unittest.main()
