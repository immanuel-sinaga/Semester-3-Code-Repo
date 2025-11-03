import cv2
import torch
import numpy as np
from pathlib import Path

class ClothesDetector:
    def __init__(self, weights_path='C:/Users/noels/Documents/AI/PoliteAttireCheck/preModelTest/yolov5/runs/train/exp2/weights/best.pt'):
        print("Initializing detector...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                  path=weights_path, force_reload=False)
        self.model.to(self.device)
        self.class_names = ["Tshirts", "Shorts", "Long Sleeve", "Trousers", "Skirts"]
        
        # Set model parameters
        self.model.conf = 0.4  # confidence threshold
        self.model.iou = 0.45   # NMS IOU threshold
        print("Detector initialized successfully!")
        
    def detect(self, frame):
        # Make prediction
        results = self.model(frame)
        
        # Process predictions
        detections = results.pred[0]
        
        if len(detections):
            for detection in detections:
                x1, y1, x2, y2 = detection[:4]
                confidence = float(detection[4])
                class_id = int(detection[5])
                
                # Draw bounding box
                cv2.rectangle(frame, 
                            (int(x1), int(y1)), 
                            (int(x2), int(y2)), 
                            (0, 255, 0), 2)
                
                # Add label
                label = f'{self.class_names[class_id]} {confidence:.2f}'
                cv2.putText(frame, label, (int(x1), int(y1-10)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame

    def run_webcam(self):
        print("Starting webcam...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
            
        print("Webcam started successfully!")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            processed_frame = self.detect(frame)
            cv2.imshow('PoliteAttireCheck', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()