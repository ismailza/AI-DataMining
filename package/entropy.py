import math

# Function to compute the logarithm base 2
def log2(x):
  return math.log(x, 2)

# Function to compute the entropy of a list of values
def entropy(values):
  result = 0.0
  div = sum(values)
  for value in values:
    if value > 0:
      result -= value/div * log2(value/div)
  return result

# Function to compute the total entropy of a list of values
def entropyTotale(values):
  result = 0.0
  total = 0
  for value in values:
    total += sum(value)
  for value in values:
    card = sum(value)
    result += entropy(value) * card / total
  return result

# Function to compute the entropy of a list of continuous values
def entropyContinu(values):
  result = 0
  total = 0
  for value in values:
    total += sum(value)
  for value in values:
    result += entropy(value) * sum(value) / total
  return result
