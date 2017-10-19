from math import *
from prettytable import PrettyTable

def func_1(x, y):
    return exp(x**3 - y) - x**3 * (x**3 - 2 * y - 2) - y**2 - 2 * y - 2

def func_2(x, y):
    return exp(2 * log(x) - y) + y * exp(-y) - exp(x**2) * log(x**2 + y)

def main():
    table = PrettyTable([" N ", " X ", " Y "])
    table1 = PrettyTable([" N ", " X ", " Y "])
    table2 = PrettyTable([" N ", " X ", " Y "])
    table3 = PrettyTable([" N ", " x(Y1 - Y2) ", " y(X) "])
    table4 = PrettyTable([" N ", " X ", " Y "])
    
    mas_x = []; mas_y = []
    tmp_x = []; tmp_y1 = []; tmp_y2 = []
    tmp_x3 = []; tmp_y3 = []

    beg = 0.1; end = 1.1
    x = beg;
    N = 20
    eps = 1e-5
    step = abs(end - beg) / N
    
    for i in range(N + 1):
        tmp_x.append(x)
        tmp_y3.append(x)
        tmp_y1.append(half_interval_root(func_1, -100, 100, eps, x))
        tmp_y2.append(half_interval_root(func_2, 0.1, 100, eps, x))
        tmp_x3.append(tmp_y1[i] - tmp_y2[i])
        x += step

    for i in range(0, len(tmp_x)):
        table1.add_row([i + 1, round(tmp_x[i], 6), round(tmp_y1[i], 6)])
        table2.add_row([i + 1, round(tmp_x[i], 6), round(tmp_y2[i], 6)])
        table3.add_row([i + 1, round(tmp_x3[i], 6), round(tmp_y3[i], 6)])
        
    print("Function 1\n", table1, "\n")
    print("Function 2\n", table2, "\n")
    print(table3, "\n")
    
    n = int(input("input n: "))
    x = float(input("input x: "))

    mas_x, mas_y  = create_new_x_y(x, n, N, tmp_x3, tmp_y3)

    for i in range(0, len(mas_x)):
        table4.add_row([i + 1, round(mas_x[i], 6), round(mas_y[i], 6)])
    print(table4)
    
    y = interpolation(x, n, mas_x, mas_y)
    y1 = half_interval_root(func_1, -100, 100, eps, y)
    y2 = half_interval_root(func_2, 0.1, 100, eps, y)
    print("\nx = ", y, "\nroot(f1) = ", y1, "\nroot(f2) = ", y2)

def create_new_x_y(x, n, N, tmp_x, tmp_y):
    mas_x = []; mas_y = []
    if (x <= tmp_x[0]):
        for i in range(0, n + 1):
            mas_x.append(tmp_x[i])
            mas_y.append(tmp_y[i])
    elif (x >= tmp_x[N]):
        for i in range(len(tmp_x) - (n + 1), len(tmp_x)):
            mas_x.append(tmp_x[i])
            mas_y.append(tmp_y[i])
    else:
        back = 0; up = 0
        for i in range(1, N):
            if((tmp_x[i - 1] <= x) and (tmp_x[i] > x)):
                up = i; back = i - 1
                for k in range(0, n + 1):
                    if (k % 2 == 0):
                        if (up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            mas_y.append(tmp_y[up])
                            up += 1
                        elif (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            mas_y.insert(0, tmp_y[back])
                            back -= 1
                    else:
                        if (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            mas_y.insert(0, tmp_y[back])
                            back -= 1
                        elif(up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            mas_y.append(tmp_y[up])
                            up += 1
    return mas_x, mas_y

def interpolation(x, n, mas_x, mas_y):
    matrix = []
    matrix.append([])
    for i in range(0, n):
        matrix[0].append((mas_y[i] - mas_y[i + 1])/(mas_x[i] - mas_x[i + 1]))
    
    m = n - 1
    for i in range(1, n):
        matrix.append([])
        for j in range(0, m):
            matrix[i].append(((matrix[i - 1][j] - matrix[i - 1][j + 1]))/(mas_x[j] - mas_x[j + 2]))     
        m -= 1

    y = mas_y[0]
    fact = 1
    for i in range(0, n):
        fact *= (x - mas_x[i])
        y += matrix[i][0] * fact
    return y

def half_interval_root(f, a, b, eps, x):  #Метод половинного деления
    fa = f(x, a)
    fb = f(x, b) 
    if fa == 0: return a
    if fb == 0: return b
    if fa * fb < 0:
        c = (a + b) / 2
        while abs(b - a) > abs(c) * eps + eps:
            c = (a + b) / 2
            fc = f(x, c)
            if fa * fc < 0:
                b = c
            else:
                a = c
        return c
    return 0
    
if __name__ == "__main__":
    main();
