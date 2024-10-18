import random
import csv

def list_random_with_order(rows, cols, min_val=1, max_val=20):
    return [[f"Job {i+1}"] + [random.randint(min_val, max_val) for _ in range(cols - 1)] for i in range(rows)]

def to_csv(data, filename='output.csv'):
    header = ['Name', 'p', 'r', 'd', 'w']
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

data1 = list_random_with_order(10, 5, min_val=1, max_val=20)

to_csv(data1, 'data1.csv')