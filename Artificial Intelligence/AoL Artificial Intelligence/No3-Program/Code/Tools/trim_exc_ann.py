import pandas as pd
import os
import random
import shutil

# Load the CSV files
styles_path = 'styles.csv'
annotated_styles_path = 'annotated_styles.csv'

# Load dataframes
styles_df = pd.read_csv(styles_path)
annotated_styles_df = pd.read_csv(annotated_styles_path)

# Set the maximum number of images per articleType
max_images_per_type = 600

# Create a folder to store the trimmed images
output_folder = 'trimmed_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize a dictionary to track the count of images for each articleType
article_type_counts = styles_df['articleType'].value_counts().to_dict()

# Get the set of image names from annotated_styles.csv to exclude from trimming
annotated_images = set(annotated_styles_df['ImageName'].astype(str))

# Process each articleType
to_remove = []
copied_images = set()

for article_type, count in article_type_counts.items():
    # Filter the DataFrame for the current articleType
    article_df = styles_df[styles_df['articleType'] == article_type]

    # If the count exceeds the limit, randomly select up to max_images_per_type images
    if count > max_images_per_type:
        sampled_df = article_df.sample(n=max_images_per_type, random_state=42)
        excess_df = article_df[~article_df['ImageName'].isin(sampled_df['ImageName'])]
        excess_df = excess_df[~excess_df['ImageName'].isin(annotated_images)]
        to_remove.extend(excess_df.index)
    else:
        sampled_df = article_df

    # Copy the selected images to the output folder
    for _, row in sampled_df.iterrows():
        image_name = f"{row['ImageName']}.jpg"
        src_image_path = os.path.join('images', image_name)
        dst_image_path = os.path.join(output_folder, image_name)
        if os.path.exists(src_image_path):
            shutil.copy(src_image_path, dst_image_path)
            copied_images.add(image_name)

# Remove excess rows from the DataFrame
trimmed_df = styles_df.drop(to_remove)

# Delete images not in the copied set and not in the annotated_styles.csv
for image_file in os.listdir('images'):
    if image_file.endswith('.jpg') and image_file not in copied_images and os.path.splitext(image_file)[0] not in annotated_images:
        image_path = os.path.join('images', image_file)
        os.remove(image_path)

# Save the trimmed CSV file
trimmed_df.to_csv('trimmed_styles.csv', index=False)

print(f"Trimmed images and CSV saved. {len(to_remove)} entries removed and unused images deleted.")
