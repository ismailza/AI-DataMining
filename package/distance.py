import pandas as pd
import numpy as np
import numbers

def manhattan_distance(l1, l2):
  return sum([abs(i - j) for i, j in zip(l1, l2)])

def jaccard_coefficient(l1, l2):
  # a is the number combinations of 1 and 0
  a = len([1 for i, j in zip(l1, l2) if i == 1 and j == 0])
  # b is the number combinations of 0 and 1
  b = len([1 for i, j in zip(l1, l2) if i == 0 and j == 1])
  # c is the number combinations of 1 and 1
  c = len([1 for i, j in zip(l1, l2) if i == j == 1])

  return (a + b) / (a + b + c)


def appariement_coefficient(l1, l2):
  # a is the number combinations of 1 and 0
  a = len([1 for i, j in zip(l1, l2) if i == 1 and j == 0])
  # b is the number combinations of 0 and 1
  b = len([1 for i, j in zip(l1, l2) if i == 0 and j == 1])
  # c is the number combinations of 1 and 1
  c = len([1 for i, j in zip(l1, l2) if i == j == 1])
  # d is the number combinations of 0 and 0
  d = len([1 for i, j in zip(l1, l2) if i == j == 0])

  return (a + b) / (a + b + c + d)


# Function to calculate the distance between two rows of a dataframe
def distance(row_a: pd.Series, row_b: pd.Series, columns: list, options: dict = {}) -> float:
  # calculate distance between row and test_data
  rest_dist = {}
  for col in columns:
    if col == 'class' or col == 'id':
      continue
    if type(row_a[col]) == list:
      if col in options and options[col] == 'jaccard':
        rest_dist[col] = jaccard_coefficient(row_a[col], row_b[col])
      else:
        rest_dist[col] = appariement_coefficient(row_a[col], row_b[col])
    elif isinstance(row_a[col], numbers.Number):
      rest_dist[col] = manhattan_distance([row_a[col]], [row_b[col]])
    else:
      print(f'error :: {col} is not a number or a list : ', type(row_a[col]), row_a[col], row_b[col])

  dist = sum(rest_dist.values()) / len(rest_dist)
  # print(f'distance of each column ::  {rest_dist} / {len(rest_dist)} -- result = {dist}')
  return dist


# Function to calculate the distance between each row of a dataframe
def calcul_distances(df: pd.DataFrame, labels: list):
  ignore_columns = []
  ignore_columns.append('id')
  ignore_columns.append('class')
  jaccard = True
  for col in df.columns:
    if col in ignore_columns:
      continue
    if not df[col].isin([0, 1]).all():
      jaccard = False
      break

  Z = np.zeros((len(labels), len(labels)))
  for i in range(len(df)):
    for j in range(i + 1, len(df)):
      if not jaccard:
        Z[i, j] = distance(df.iloc[i], df.iloc[j], columns=df.columns)
      else:
        Z[i, j] = jaccard_coefficient(df.iloc[i], df.iloc[j])
      Z[j, i] = Z[i, j]
  return Z
