import pandas as pd

# Paths to the CSV files
styles_path = 'styles.csv'
styles1_path = 'styles1.csv'
output_path = 'combined_styles.csv'

# Load both CSV files into dataframes
styles_df = pd.read_csv(styles_path)
styles1_df = pd.read_csv(styles1_path)

# Concatenate the two dataframes
combined_df = pd.concat([styles_df, styles1_df])

# Remove duplicate rows based on all columns
combined_df = combined_df.drop_duplicates()

# Save the combined dataframe to a new CSV file
combined_df.to_csv(output_path, index=False)

print(f"Combined styles saved to {output_path}.")
