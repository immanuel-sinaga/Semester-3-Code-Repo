import os
import pandas as pd

# Define paths
csv_path = 'styles.csv'
image_folder = 'images'

# Load CSV while skipping problematic lines
df = pd.read_csv(csv_path, on_bad_lines='skip')

# Filter rows where:
# 1. 'masterCategory' contains 'Apparel' (case insensitive)
# 2. 'subCategory' is not 'Innerwear'
# 3. 'articleType' is not 'Swimwear'
filtered_df = df[(df['masterCategory'].str.contains('Apparel', case=False, na=False)) & 
                 (df['subCategory'] != 'Innerwear')]

# Extract the IDs of the images that meet the condition
apparel_ids = filtered_df['id'].astype(str).tolist()

# List all image files in your folder
image_files = os.listdir(image_folder)

# Remove images that do not match any ID in the filtered DataFrame
for img_file in image_files:
    image_id = img_file.replace('.jpg', '').replace('.png', '')
    if image_id not in apparel_ids:
        os.remove(os.path.join(image_folder, img_file))

# Save the filtered data back to a new CSV
filtered_df.to_csv('filtered_apparel_data.csv', index=False)

print(f"Filtered dataset saved with {len(filtered_df)} entries.")