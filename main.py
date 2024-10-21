import tilearn as tl
from tilearn import _plat as pl

data = '/Users/chibangnguyen/Documents/thuhoach.nckh/data'
backup = '/Users/chibangnguyen/Documents/thuhoach.nckh/data/backup'
data1 = '/Users/chibangnguyen/Documents/thuhoach.nckh/data/data1.csv'

list = [
    pl.List(file_path=data1, prec=0)
]

schedule = tl.optimal_list(list, data, backup)

for row in schedule:
    print(row)