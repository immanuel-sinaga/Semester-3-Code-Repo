import pandas as pd

# Load the filtered CSV file
input_file = 'styles.csv'  # The file created earlier
output_file = 'filtered_styles.csv'  # Output file name

# Read the CSV file
data = pd.read_csv(input_file)

# Drop the 'masterCategory' column
filtered_data = data.drop(columns=['masterCategory'])

# Save the updated data to a new CSV file
filtered_data.to_csv(output_file, index=False)

print(f"CSV without 'masterCategory' column saved as: {output_file}")
