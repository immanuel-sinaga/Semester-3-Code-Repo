import os
import pandas as pd

# Define the path to the images folder and the CSV file
image_folder = 'images'
csv_file = 'styles.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Get the list of image filenames (with extensions) in the images folder
image_files = {os.path.splitext(f)[0]: f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))}

# Keep only rows in the CSV that match the existing images
df_filtered = df[df['ImageName'].astype(str).isin(image_files.keys())]

# Preview what will be deleted
orphan_images = [image_files[name] for name in image_files.keys() if name not in df['ImageName'].astype(str).values]
orphan_csv_entries = df[~df['ImageName'].astype(str).isin(image_files.keys())]

print("Images to be deleted:")
for image in orphan_images:
    print(image)

print("\nCSV entries to be removed:")
print(orphan_csv_entries)

# Confirm before making changes
confirm = input("\nProceed with the cleanup? (yes/no): ").strip().lower()
if confirm == 'yes':
    # Save the filtered DataFrame back to the CSV
    df_filtered.to_csv(csv_file, index=False)
    print(f"Updated CSV file saved to {csv_file}.")

    # Delete orphan images
    for image in orphan_images:
        image_path = os.path.join(image_folder, image)
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
else:
    print("No changes made.")
