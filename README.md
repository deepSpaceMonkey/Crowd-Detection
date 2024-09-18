# Crowd Size Estimation Using YOLOv8: Project Overview and Reflections

## Project Workflow

The project was structured into several modular components to ensure scalability and maintainability:

1. **Video Preparation:** Trimming the original drone footage to focus on the area of interest and removing unnecessary audio tracks.
2. **Frame Extraction:** Extracting specific frames at predetermined timestamps to analyze snapshots of the crowd.
3. **Preprocessing:** Resizing and normalizing frames to meet YOLOv8’s input specifications.
4. **Model Setup:** Integrating the YOLOv8 model using the `ultralytics` library for object detection.
5. **Object Detection:** Running the YOLOv8 model on preprocessed frames to identify and localize individuals.
6. **Post-Processing:** Filtering detections based on confidence thresholds to enhance accuracy.
7. **Counting:** Aggregating detections to estimate the total crowd size.

## Challenges Faced

1. **Initial Learning Curve:** As a first-time project in computer vision, navigating the complexities of deep learning frameworks, understanding YOLOv8’s intricacies, and integrating various modules presented a steep learning curve.
2. **Black Screen Issue:** During video preparation, a black screen was observed in the initial 1.5 seconds of the trimmed video. This was due to the encoding used, so I switched to re-encoding the video to the H.264 codec to avoid the black screen.
3. **Double Counting:** I considered taking multiple frames and averaging out the count from each frame; however, the drone pans across the entire bridge, resulting in varying densities of people. As a quick fix, I manually chose two frames that did not overlap at all. This was the best solution given the time constraints and my skillset. This approach would be improved in the future.
4. **Scale Variation:** The drone’s varying altitudes and angles cause individuals to appear at different scales within frames. Maintaining consistent detection accuracy across these scale variations necessitates careful parameter tuning and potentially multi-scale detection strategies.
5. **Model Generalization:** I likely chose a pre-trained model that was too general. Additionally, the model was not fine-tuned sufficiently on my part, which may have affected detection accuracy.

## Potential Improvements (Things I'd Do Differently)

1. **Spatial Segmentation for Double Counting Prevention:** Dividing the scene into distinct regions and tracking individuals across frames can prevent double counting. Techniques like region-based detection or tracking algorithms (e.g., SORT, Deep SORT) can be integrated to maintain unique counts within each region.
2. **Zooming in on Frames Before Sending to YOLO Model:** To address the scale variation issue, enlarging each frame can make individuals more discernible to the detection model. Additionally, applying dynamic scaling techniques to adjust the size of detected objects based on their position or distance can enhance detection accuracy across varying scales.
3. **Adaptive Lighting Correction:** Implementing preprocessing steps like histogram equalization or adaptive thresholding can mitigate the impact of varying lighting conditions, thereby enhancing frame quality for better detection.

## Lessons Learned

- **Modular Design Benefits:** Structuring the project into discrete modules facilitated focused development, easier debugging, and scalability. Each module could be developed and tested independently, streamlining the overall workflow.
- **Importance of Preprocessing:** Much of the accuracy from data science models comes from the quality of the input data. Effective preprocessing—resizing, normalization, and noise reduction—proved crucial in enhancing frame quality and ensuring compatibility with the YOLOv8 model.
- **Model Selection and Configuration:** Understanding the nuances of YOLOv8, including model variants and configuration parameters, was essential in optimizing detection performance for the specific application context.
- **Handling Real-World Variability:** Addressing real-world challenges such as occlusions, varying lighting, and motion blur underscored the importance of robust preprocessing and adaptable model configurations.
- **Value of Comprehensive Logging:** Implementing detailed logging at each pipeline step facilitated real-time monitoring, easier identification of issues, and a better understanding of the system’s performance.
- **Iterative Development Approach:** Adopting an incremental development and Git commit strategy enabled systematic progress tracking, risk mitigation, and facilitated easier collaboration or future enhancements.

## Conclusion

This project marked an insightful foray into computer vision and deep learning, particularly in applying YOLOv8 for practical crowd size estimation from drone footage. While the initial results did not yield successful detections, the structured modular approach, coupled with detailed logging and systematic development practices, laid a solid foundation for future improvements. Addressing the identified challenges and implementing the proposed enhancements will pave the way for more accurate and reliable crowd size estimation in subsequent iterations. Embracing iterative testing, continuous learning, and adaptive strategies will be key to overcoming obstacles and achieving the project’s objectives in real-world applications.