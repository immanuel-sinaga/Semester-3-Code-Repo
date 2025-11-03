import pandas as pd
import os

# Load the styles.csv and annotated_styles.csv files
styles_path = 'styles.csv'
annotated_styles_path = 'annotated_styles.csv'
images_folder = 'images'

# Load CSVs into dataframes
styles_df = pd.read_csv(styles_path)
annotated_styles_df = pd.read_csv(annotated_styles_path)

# Filter for relevant articleTypes
article_types_to_remove = {'Tops', 'Dresses', 'Shirts'}

# Get ImageName set from annotated_styles.csv to keep
annotated_images = set(annotated_styles_df['ImageName'].astype(str))

# Filter styles.csv based on conditions
filtered_styles_df = styles_df[
    ~(
        (styles_df['articleType'].isin(article_types_to_remove)) &
        (~styles_df['ImageName'].astype(str).isin(annotated_images))
    )
]

# Find image files to remove
all_images_in_folder = set(os.listdir(images_folder))
images_to_remove = set(styles_df.loc[
    styles_df['articleType'].isin(article_types_to_remove) &
    ~styles_df['ImageName'].astype(str).isin(annotated_images), 'ImageName'
].astype(str) + '.jpg')  # Assuming the images have .jpg extension

# Remove image files
for image in images_to_remove:
    image_path = os.path.join(images_folder, image)
    if os.path.exists(image_path):
        os.remove(image_path)

# Save the filtered dataframe back to styles.csv
filtered_styles_df.to_csv(styles_path, index=False)

print(f"Filtered styles.csv saved. {len(images_to_remove)} image files removed.")
