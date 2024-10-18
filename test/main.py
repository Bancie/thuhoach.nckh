import random
import csv

def list_random(rows, cols, min=0, max=100):
    return [[random.randint(min, max) for _ in range(cols)] for _ in range(rows)]

def to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

list = list_random(5, 5, min=10, max=50)
to_csv(list, '/Users/chibangnguyen/Documents/thuhoach.nckh/test/random_data.csv')