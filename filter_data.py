import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('src/data/imdb_full.csv')

# Ensure the release year column is of integer type
df['releaseYear'] = pd.to_numeric(df['releaseYear'], errors='coerce')

# Filter the DataFrame for titles made from 2022 and onward
filtered_df = df[df['releaseYear'] >= 2022]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('src/data/imdb_filtered2022.csv', index=False)

print("Filtered dataset saved to 'data/imdb_filtered.csv'")