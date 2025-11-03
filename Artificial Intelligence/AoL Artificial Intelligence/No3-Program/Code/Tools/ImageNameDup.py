import pandas as pd

# Path to the CSV file
csv_path = 'annotated_styles.csv'

# Load the CSV file
data = pd.read_csv(csv_path)

# Check for duplicate ImageName entries
duplicates = data[data.duplicated(subset=['ImageName'], keep=False)]

if not duplicates.empty:
    print("Duplicate ImageName entries found:")
    print(duplicates)
else:
    print("No duplicate ImageName entries found.")

# Save duplicates to a separate CSV for further inspection
duplicates.to_csv('duplicates.csv', index=False)