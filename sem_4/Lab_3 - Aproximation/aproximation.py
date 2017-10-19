from collections import namedtuple
from prettytable import PrettyTable
import copy

def funct(x, n):
    return x ** n

#Работа с таблицей
def print_table(data):
    table = PrettyTable([" N ", " X ", " Y ", " W "])
    for i in range(len(data)):
        table.add_row([i + 1, round(data[i][0], 6), round(data[i][1], 6), round(data[i][2],6)])
    print(table)

def fread_table(fname, Table):
    file = open(fname)
    data = []
    
    for line in file:
        a, b, c = map(float, line.split())
        data.append(Table(a, b, c))
                
    file.close()
    return data


#--------------------------------

# Вывод графика аппроксимирующей функции и исходных точек
def print_result(table, A, n):
    import numpy as np
    import matplotlib.pyplot as plt
    dx = 10
    if len(table) > 1:
        dx = (table[1].x - table[0].x)

    # построение аппроксимирующей функции    
    x = np.linspace(table[0].x - dx, table[-1].x + dx, 100)
    y = []
    for i in x:
        tmp = 0;
        for j in range(0, n + 1):
            tmp += funct(i, j) * A[j]
        y.append(tmp)

    plt.plot(x, y)

    #построение исходной таблицы
    x1 = [a.x for a in table]
    y1 = [a.y for a in table]


    plt.plot(x1, y1, 'kD', color = 'green', label = 'dots')
    
    plt.grid(True)
    plt.legend(loc = 'best')
    miny = min(min(y), min(y1))
    maxy = max(max(y), max(y1))
    dy = (maxy - miny) * 0.03
    plt.axis([table[0].x - dx, table[-1].x + dx, miny - dy, maxy + dy])

    plt.show()
    return 

# получение СЛАУ по исходным данным для заданной степени
# возвращает матрицу коэф. и столбец свободных членов
def get_slau_matrix(table, n):
    N = len(table)
    matrix = [[0] * (n + 1) for j in range (0, n + 1)]
    col = [0] * (n + 1)

    '''for i in range(n + 1): 
        for j in range(n + 1): 
            sum = 0
            for k in range(N):
                sum += table[k].w * pow(table[k].x, i + j);
            matrix[i][j] = sum;
        
        sum = 0
        for k in range(N):
            sum += table[k].w * table[k].y * pow(table[k].x, i);
    
        col[i] = sum;'''
    
    
    for m in range(0, n + 1):
        for i in range(0, N):
            tmp = table[i].w * funct(table[i].x, m)
            for k in range(0, n + 1):
                matrix[m][k] += tmp * funct(table[i].x, k)
            col[m] += tmp * table[i].y
            
    return matrix, col

'''def gaussmethod(result, matrix, coefs):
    result.clear();
    size = len(matrix)
    result = [0] * size

    #forward
    for i in range(size):
        if (matrix[i][i] == 0):
            swapped = False
            for j in range(i + 1, size):
                if (matrix[j][i] != 0):
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    swapped = True
                    break
            if (swapped == False):
                return 1
        for j in range(i + 1, size):
            if (matrix[j][i] == 0):
                continue
            
            coef = matrix[i][i] / matrix[j][i]
            for m in range(i, size):
                matrix[j][m] *= coef
                matrix[j][m] -= matrix[i][m]
            
            coefs[j] *= coef
            coefs[j] -= coefs[i]
        
    #backward
    print("------")
    for i in reversed(range(0, size)):
        suma = 0
        for j in range(i, size):
            suma += matrix[i][j] * result[j]
            print(suma, matrix[i][j], result[j])
            
        result[i] = (coefs[i] - suma) / matrix[i][i]
        #print(coefs[i], suma, matrix[i][i])
    #print("______", result)
    #print("\n", coefs)
    return 0'''

# поиск столбца обратной матрицы
def find_col(matrix_tmp, i_col):
    n = len(matrix_tmp)
    matrix = copy.deepcopy(matrix_tmp)
    col = [0] * n
    
    for i in range(0, n):
        matrix[i].append(float(i == i_col))
    for i in range(0, n):
        if matrix[i][i] == 0: 
            for j in range(i + 1, n):
                if matrix[j][j] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
        for j in range(i + 1, n):
            d = - matrix[j][i] / matrix[i][i]
            for k in range(0, n + 1):
                matrix[j][k] += d * matrix[i][k]
    for i in range(n - 1, -1, -1):
        res = 0
        for j in range(0, n):
            res += matrix[i][j] * col[j]
        col[i] = (matrix[i][n] - res) / matrix[i][i]
    return col

# умножение столбца на матрицу
def multiplication(col, b):
    n = len(col)
    new_col = [0] * n
    for i in range(0, n):
        for j in range(0, n):
            new_col[i] += col[j] * b[i][j]
    return new_col
    
# получение обратной матрицы
def get_inverse_matrix(a):
    n = len(a)
    matrix = [[0] * n for j in range (0, n)]

    for i in range(0, n):
        col = find_col(a, i)
        for j in range(0, n):
            matrix[j][i] = col[j]
    return matrix

# получение коэф. аппроксимирующей функции
def get_approx_coef(table, n):
    m, z = get_slau_matrix(table, n)
    #koef = []
    #gaussmethod(koef, m, z)
    inv = get_inverse_matrix(m)
    koef = multiplication(z, inv)
    return koef


def main():
    Table = namedtuple('Table', ['x','y', 'w'])
    fname = input("Введите название файла: ") + ".txt"
    table = fread_table(fname, Table)
    print_table(table)

    n = int(input("Введите степень полинома n = "))
    A = get_approx_coef(table, n)
    
    print_result(table, A, n)


if __name__ == "__main__":
    main()
