import pandas as pd

# Load the CSV file
df = pd.read_csv('styles.csv', on_bad_lines='skip')

# Get unique article types
unique_article_types = df['articleType'].unique()

# Print out the distinct article types
print("Distinct Article Types:")
for article_type in sorted(unique_article_types):
    print(f"- {article_type}")

# Optional: Count of each article type
print("\nArticle Type Counts:")
article_type_counts = df['articleType'].value_counts()
print(article_type_counts)