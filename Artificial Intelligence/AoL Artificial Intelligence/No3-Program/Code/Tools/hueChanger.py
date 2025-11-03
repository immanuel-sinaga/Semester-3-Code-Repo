import os
import pandas as pd
import cv2
import random
import numpy as np

def apply_hue_shift(image, shift):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] = (hsv[:, :, 0] + shift) % 180
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def process_skirts(csv_path, image_dir, output_dir):
    df = pd.read_csv(csv_path)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    
    skirts_df = df[df['articleType'] == 'Skirts']
    augmented_rows = []
    
    for _, row in skirts_df.iterrows():
        img_path = os.path.join(image_dir, f"{row['ImageName']}.jpg")
        if not os.path.exists(img_path):
            continue
            
        image = cv2.imread(img_path)
        shifts = random.sample([-30, -15, 15, 30], 2)
        
        for i, shift in enumerate(shifts, 1):
            augmented_image = apply_hue_shift(image, shift)
            new_img_name = f"{row['ImageName']}111{i}"
            
            cv2.imwrite(
                os.path.join(output_dir, 'images', f"{new_img_name}.jpg"),
                augmented_image
            )
            
            new_row = row.copy()
            new_row['ImageName'] = new_img_name
            augmented_rows.append(new_row)
    
    augmented_df = pd.DataFrame(augmented_rows)
    augmented_df.to_csv(os.path.join(output_dir, "styles.csv"), index=False)

if __name__ == "__main__":
    process_skirts(
        csv_path='styles.csv',
        image_dir='images',
        output_dir='augmented_dataset'
    )