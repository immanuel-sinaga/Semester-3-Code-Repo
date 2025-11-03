import os
import pandas as pd
import shutil

class LabelConverter:
    def __init__(self, csv_path, images_folder, output_folder):
        self.csv_path = csv_path
        self.images_folder = images_folder
        self.output_folder = output_folder
        self.class_names = ["Tshirts", "Shorts", "Long Sleeve", "Trousers", "Skirts"]
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.class_names)}
        
    def create_yolo_labels(self):
        """Converts the dataset into YOLOv5 format."""
        # Load CSV
        df = pd.read_csv(self.csv_path)
        
        # Create output directories for images and labels
        images_output_path = os.path.join(self.output_folder, "images")
        labels_output_path = os.path.join(self.output_folder, "labels")
        os.makedirs(images_output_path, exist_ok=True)
        os.makedirs(labels_output_path, exist_ok=True)
        
        for _, row in df.iterrows():
            image_name = f"{row['ImageName']}.jpg"
            class_name = row['articleType']
            
            # Check if class_name exists in class_to_idx
            if class_name not in self.class_to_idx:
                print(f"Skipping unknown class: {class_name}")
                continue
            
            # Copy image to the output folder
            src_image_path = os.path.join(self.images_folder, image_name)
            dst_image_path = os.path.join(images_output_path, image_name)
            
            if not os.path.exists(src_image_path):
                print(f"Image not found: {src_image_path}")
                continue
            
            shutil.copy2(src_image_path, dst_image_path)
            
            # Create YOLO label
            class_id = self.class_to_idx[class_name]
            label_content = f"{class_id} {row['a']} {row['b']} {row['c']} {row['d']}\n"
            
            label_file_path = os.path.join(labels_output_path, f"{row['ImageName']}.txt")
            with open(label_file_path, "w") as label_file:
                label_file.write(label_content)
        
        print(f"Labels and images saved to {self.output_folder}")

# Example usage
csv_path = "styles.csv"  # Path to your styles.csv file
images_folder = "images"  # Path to your images folder
output_folder = "dataset"  # Output folder for YOLO dataset

converter = LabelConverter(csv_path, images_folder, output_folder)
converter.create_yolo_labels()
