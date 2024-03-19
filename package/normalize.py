import pandas as pd

def normalize_data(df: pd.DataFrame, test_date: pd.DataFrame = None, ignore_cols: list = []):
  ignore_cols.append('class')
  ignore_cols.append('id')
  numeric_cols = df.select_dtypes(include='number').columns
  numeric_cols = [col for col in numeric_cols if col not in ignore_cols]

  for col in numeric_cols:
    vals = df[col]
    minValue = min(vals)
    maxValue = max(vals)
    if 0 <= minValue and maxValue <= 1:
      continue
    denom = maxValue - minValue

    df[col] = df.apply(lambda row: (row[col] - minValue) / denom, axis = 1)
    if test_date is not None:
      test_date[col] = test_date.apply(lambda row: (row[col] - minValue) / denom, axis=1)

  non_numeric_cols = df.select_dtypes(include='object').columns.tolist()
  non_numeric_cols = [col for col in non_numeric_cols if col not in ignore_cols]

  for col in non_numeric_cols:
    uniq_vals = df[col]
    uniq_vals = uniq_vals.unique()
    print(f'normilize order of "{col}" :: {uniq_vals}')
    vals_map = {}
    for val in range(len(uniq_vals)):
      vals_map[uniq_vals[val]] = [0] * len(uniq_vals)
      vals_map[uniq_vals[val]][val] = 1

    df[col] = df.apply(lambda row: vals_map[row[col]], axis=1)
    if test_date is not None:
      test_date[col] = test_date.apply(lambda row: vals_map[row[col]], axis=1)
