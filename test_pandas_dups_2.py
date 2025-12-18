import pandas as pd

print("Pandas version:", pd.__version__)

# Scenario: Source has duplicate columns
df = pd.DataFrame([[1, 2, 3, 4]], columns=["A", "B", "B", "C"])
print("Source columns:", df.columns.tolist())

keep_cols = ["A", "B", "B"] # User explicitly lists B twice

cols_to_select = [col for col in keep_cols if col in df.columns]
# "B" is in df.columns (it returns True if any match)

# Selection
# df[cols_to_select] ??
# cols_to_select will be ['A', 'B', 'B']
# df[['A', 'B', 'B']]
# df['B'] returns a DataFrame with 2 columns.
# Selecting ['A', 'B', 'B'] should produce:
# Col A (1)
# Col B (2 cols)
# Col B (2 cols)
# Total 5 columns?

df_subset = df[cols_to_select]
print("Subset columns:", df_subset.columns.tolist())

df_subset2 = df_subset.copy()

try:
    pd.concat([df_subset, df_subset2], ignore_index=True)
    print("Concat success")
except Exception as e:
    print("Concat failed:", e)
