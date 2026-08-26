import pandas as pd
import os

# Define file paths
data_dir = r"c:\Users\thrix\Documents\flappy-rf\data\raw"
file1_path = os.path.join(data_dir, "dataset.csv")
file2_path = os.path.join(data_dir, "raw_dataset.csv")
output_path = os.path.join(data_dir, "cdataset.csv")

headers = ["dist_x", "dist_y", "axis_y", "vel_y", "action"]

# 1. Load both CSV files
# Note: If your CSVs already contain header rows, remove `names=headers, header=0`
df1 = pd.read_csv(file1_path, names=headers, header=0)
df2 = pd.read_csv(file2_path, names=headers, header=0)

print(f"Loaded dataset.csv: {len(df1)} rows")
print(f"Loaded raw_dataset.csv: {len(df2)} rows")

# 2. Concatenate vertically (row-wise stack)
combined_df = pd.concat([df1, df2], ignore_index=True)

# 3. Clean up duplicates and empty rows
combined_df = combined_df.dropna().drop_duplicates().reset_index(drop=True)

# 4. Save merged dataset
os.makedirs(os.path.dirname(output_path), exist_ok=True)
combined_df.to_csv(output_path, index=False)

print(f"Successfully saved combined dataset with {len(combined_df)} rows to {output_path}")