import cv2
import pandas as pd
import os

# Paths
csv_path = 'styles.csv'
images_folder = 'images'
output_csv = 'annotated_styles.csv'

# Load existing annotations or create a new one
if os.path.exists(output_csv):
    annotated_df = pd.read_csv(output_csv)
    # Remove any duplicate entries based on ImageName
    annotated_df = annotated_df.drop_duplicates(subset=['ImageName'], keep='first')
else:
    annotated_df = pd.DataFrame(columns=['ImageName', 'subCategory', 'articleType', 'a', 'b', 'c', 'd'])

# Load the original CSV
data = pd.read_csv(csv_path)

# Define mouse callback variables
drawing = False
bbox = None
x_start, y_start = -1, -1
cursor_pos = (-1, -1)

def draw_bbox(event, x, y, flags, param):
    global x_start, y_start, drawing, bbox, cursor_pos
    cursor_pos = (x, y)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            bbox = (x_start, y_start, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bbox = (x_start, y_start, x, y)

# Filter out already annotated images
processed_images = set(annotated_df['ImageName'].values)
remaining_data = data[~data['ImageName'].isin(processed_images)]

# Iterate through the images
for index, row in remaining_data.iterrows():
    image_name = f"{row['ImageName']}"
    subcategory = row['subCategory']
    articletype = row['articleType']
    
    # Check if the image exists
    image_path = None
    for ext in ['.jpg', '.jpeg', '.png']:
        potential_path = os.path.join(images_folder, f"{image_name}{ext}")
        if os.path.exists(potential_path):
            image_path = potential_path
            break
            
    if not image_path:
        print(f"Image {image_name} not found, skipping.")
        continue

    # Load and resize the image to fit the screen
    img = cv2.imread(image_path)
    clone = img.copy()
    height, width = img.shape[:2]
    max_dim = 800
    scale = min(max_dim / width, max_dim / height)
    resized_img = cv2.resize(img, (int(width * scale), int(height * scale)))
    clone = resized_img.copy()
    
    bbox = None
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_bbox)
    
    while True:
        temp_img = clone.copy()
        if bbox:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(temp_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
        # Draw horizontal and vertical guide lines
        cursor_x, cursor_y = cursor_pos
        if cursor_x >= 0 and cursor_y >= 0:
            cv2.line(temp_img, (cursor_x, 0), (cursor_x, temp_img.shape[0]), (255, 0, 0), 1)
            cv2.line(temp_img, (0, cursor_y), (temp_img.shape[1], cursor_y), (255, 0, 0), 1)
            
        cv2.imshow("Image", temp_img)
        key = cv2.waitKey(1) & 0xFF
        
        if key == 13:  # Enter key
            if bbox:
                # Normalize coordinates to YOLO format
                img_h, img_w = resized_img.shape[:2]
                x1, y1, x2, y2 = bbox
                x_center = ((x1 + x2) / 2) / img_w
                y_center = ((y1 + y2) / 2) / img_h
                width = abs(x2 - x1) / img_w
                height = abs(y2 - y1) / img_h
                
                # Add to annotations
                new_row = pd.DataFrame({
                    'ImageName': [image_name],
                    'subCategory': [subcategory],
                    'articleType': [articletype],
                    'a': [x_center],
                    'b': [y_center],
                    'c': [width],
                    'd': [height]
                })
                annotated_df = pd.concat([annotated_df, new_row], ignore_index=True)
                # Save incrementally
                annotated_df.to_csv(output_csv, index=False)
            break
            
        elif key == 27:  # Escape key
            cv2.destroyAllWindows()
            exit()
            
    cv2.destroyAllWindows()