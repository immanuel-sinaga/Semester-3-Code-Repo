import pandas as pd

# Load the annotated_styles.csv file
annotated_styles_path = 'annotated_styles.csv'

# Load CSV into a dataframe
annotated_styles_df = pd.read_csv(annotated_styles_path)

# Filter for relevant articleTypes
article_types_to_remove = {'Tops', 'Dresses', 'Shirts'}

# Filter out entries with specified articleTypes
filtered_annotated_styles_df = annotated_styles_df[
    ~annotated_styles_df['articleType'].isin(article_types_to_remove)
]

# Save the filtered dataframe back to annotated_styles.csv
filtered_annotated_styles_df.to_csv(annotated_styles_path, index=False)

print("Filtered annotated_styles.csv saved.")
