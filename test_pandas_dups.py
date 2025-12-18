import pandas as pd

# Scenario 1: Unique columns in source, requested duplicates
df1 = pd.DataFrame({'A': [1], 'B': [2]})
keep_cols = ['A', 'A']
df_subset1 = df1[keep_cols]
print("Scenario 1 columns:", df_subset1.columns.tolist())

# Scenario 2: Duplicate columns in source
df2 = pd.DataFrame([[1, 2, 3]], columns=['A', 'A', 'B'])
print("Scenario 2 original columns:", df2.columns.tolist())
# keep_cols = ['A'] -> selects both As?
try:
    df_subset2 = df2[['A']]
    print("Scenario 2 subset columns:", df_subset2.columns.tolist())
except Exception as e:
    print("Scenario 2 error:", e)

# Scenario 3: Concat with duplicates
df3 = df_subset1.copy()
df4 = df_subset1.copy()
try:
    pd.concat([df3, df4], ignore_index=True)
    print("Concat success")
except Exception as e:
    print("Concat error:", e)
