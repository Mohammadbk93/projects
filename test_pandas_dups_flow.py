import pandas as pd

# Create a DataFrame with duplicate column names
df = pd.DataFrame([[1, 2, 3]], columns=['A', 'B', 'B'])
print("Original columns:", df.columns.tolist())

# Simulate the user's keep_cols logic
keep_cols = ['A', 'B', 'B']
selected_cols = [col for col in keep_cols if col in df.columns]
print("Selected cols list:", selected_cols)

# Select from DataFrame
try:
    df_subset = df[selected_cols]
    print("Subset columns:", df_subset.columns.tolist())
    print("Subset shape:", df_subset.shape)
except Exception as e:
    print("Selection error:", e)

# Test the rename-concat-restore flow
def make_cols_unique(d):
    cols = pd.Series(d.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [
            dup + (f".{i}" if i > 0 else "") 
            for i in range(sum(cols == dup))
        ]
    d.columns = cols
    return d

df_sub1 = df_subset.copy()
df_sub2 = df_subset.copy()

print("\n--- Applying Fix ---")
df_sub1 = make_cols_unique(df_sub1)
print("Unique cols sub1:", df_sub1.columns.tolist())

df_final = pd.concat([df_sub1, df_sub1], ignore_index=True) # Concatenating with itself for simplicity
print("Concat result cols:", df_final.columns.tolist())

# Restore
df_final.columns = df_final.columns.str.replace(r"\.\d+$", "", regex=True)
print("Restored cols:", df_final.columns.tolist())

# Check if to_excel preserves them
df_final.to_excel("test_dups.xlsx", index=False)
# Read back
df_read = pd.read_excel("test_dups.xlsx")
print("Read back cols:", df_read.columns.tolist())
