from math import *
from prettytable import PrettyTable
import bisect

def func(x):
    return 1 / (1 + x * x)

class KoefData:
    a = b = c = d = 0

class ProgonData:
    alpha = beta = 0
    
def create_koef_abcd(x, y):
    len_data = len(x) - 1
    koef_data = []
    progon_data = []
    for i in range(0, len_data):
        koef_data.append(KoefData())
        progon_data.append(ProgonData())
    
    progon_data[0].alpha = progon_data[0].beta = 0
    for i in range(1, len_data):
        A = x[i] - x[i - 1]
        B = (-2) * (x[i + 1] - x[i - 1])
        C = x[i + 1] - x[i]
        F = (-3) * ((y[i + 1] - y[i]) / C - (y[i] - y[i - 1]) / A) 

        z = B - A * progon_data[i - 1].alpha
        progon_data[i].alpha = C / z
        progon_data[i].beta = (F + A * progon_data[i - 1].beta) / z
    
    dx = x[len_data] - x[len_data - 1]
    koef_data[len_data - 1].c = 0
    koef_data[len_data - 1].a = y[len_data - 1]
    koef_data[len_data - 1].b = (y[len_data] - y[len_data  - 1]) / dx
    koef_data[len_data - 1].d = 0
   
    for i in reversed(range(0, len_data - 1)):
        dx = x[i + 1] - x[i]
        koef_data[i].c = (progon_data[i + 1].alpha *
                koef_data[i + 1].c + progon_data[i + 1].beta)
        koef_data[i].a = y[i]
        koef_data[i].b = ((y[i + 1] - y[i]) / dx - dx *
                (koef_data[i + 1].c + 2 * koef_data[i].c) / 3)
        koef_data[i].d = (koef_data[i + 1].c - koef_data[i].c) / (3 * dx)
    return koef_data;

def splain(koef, tmp_x, x):
    ind = bisect.bisect_left(tmp_x, x) - 1
    h = x - tmp_x[ind]
    return (koef[ind].a + koef[ind].b * h + 
               koef[ind].c * h**2 + koef[ind].d * h**3)

def main():
    tmp_x = []; tmp_y = [];
    beg = 0; end = 1
    step = 1
    tmp = beg
    
    while (tmp <= end):
        tmp_x.append(tmp)
        tmp_y.append(func(tmp))
        tmp += step

    table = PrettyTable(["N", "X", "Y"])
    for i in range(0, len(tmp_x)):
        table.add_row([i + 1, tmp_x[i], tmp_y[i]])
    print(table)

    len_data = len(tmp_x) - 1
    x = float(input("input x: "))
    print("Result: ", splain(create_koef_abcd(tmp_x, tmp_y), tmp_x, x))
    print("Real Result: ", func(x))

if __name__ == "__main__":
    main();
