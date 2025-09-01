import numpy as np

data = []
for i in range(5):
    row_vals = []
    for j in range(5):
        idx = i * 5 + j
        row_vals.append(5)
    data.append(row_vals)

print(data)

# for row in data:
#     print(row)