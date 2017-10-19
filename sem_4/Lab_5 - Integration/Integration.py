from math import cos, pi, exp, sqrt
from prettytable import PrettyTable
import numpy as np

eps = 0.0001
def f(x):
    return exp(-x * x / 2)

def print_table(x, k_w, k_f):
    table = PrettyTable(["N", "Корни полинома Лежандра",\
                "Весовые коэф. по формуле",\
                    "Коэф. по решению системы"])
    for i in range(len(x)):
        table.add_row([i + 1, x[i], k_w[i], k_f[i]])
    print(table)
    
def get_polinom_Legendre(n, x):
    p = []
    p.append(1)
    p.append(x)
    
    for i in range(2, n + 1):
        tmp = (2 * i - 1) * x * p[i - 1] - (i - 1) * p[i - 2]
        tmp /= i
        p.append(tmp)
        
    return p

def get_deveration_polinom_Legendre(n, p, x):
    return n / (1 - x * x) * (p[n - 1] - x * p[n])

# можно оптимизировать поиском первой половины корней
def get_roots_Legendre(n):

	# если i брать в ест. порядке, то получится от большего к меньшему
    x = [cos(pi * (4 * i - 1) / (4 * n + 2)) for i in range(n, 0, -1)]     
#    print(x)
    px = []
    dpx = []
    for i in range(0, n):
        p = []
        dp = []
        while True:
            p  = get_polinom_Legendre(n, x[i])
            dp = get_deveration_polinom_Legendre(n, p, x[i])
            dx = p[n] / dp
            x[i] -= dx
            if abs(dx) < eps:
                break
        px.append(p)
        dpx.append(dp)
    return x, px, dpx

def get_coef_Gauss_formula(x, dp, n):
    def getA(i):
        return 2 / (1 - x[i] * x[i]) / (dp[i] * dp[i]) 

    a = [getA(i) for i in range(0, n)]
    return a

def get_coef_Gauss(x, n):
    z = []
    for i in range(0, n):
        if i % 2 == 0:
            z.append(2 / (i + 1))
        else:
            z.append(0)

    matr = []
    matr.append([1 for i in range(0, n)])
    for i in range(1, n):
        matr.append([])
        for j in range (0, n):
            matr[i].append(matr[i-1][j] * x[j])
    res = np.linalg.solve(matr, z) ########
    return res
    
def F(x, alpha, t, weights):
	res = 0
	n = len(t)
	for i in range(0, n):
		res += weights[i] * f((x / 2) * (t[i] + 1)) ## modife if lower limit is not 0
	res *= (x / 2)
	return res - alpha


#a, b - значения для поиска (а = 0) 
def find_limit_of_integration(a, b, alpha, t, weights):
	#print(a, F(a, alpha, t, weights)) #NO
	#print(alpha) #NO
	if(F(a, alpha, t, weights) > 0):
		a, b = b, a
	if(F(a, alpha, t, weights) > 0):
		print("Увеличить диапазон поиска!")
		return
	tmp = 0
	j = 0
#	while True:
	while j < 10:
		#j += 1
		tmp = (a + b) / 2
		Ftmp = F(tmp, alpha, t, weights)
		#print(tmp, Ftmp) #NO

		if abs((b - tmp) / b) < eps:
			break
		if Ftmp < 0:
			a = tmp
		else:
			b = tmp
	return tmp

def main():
    n = int(input("n = "))
    alpha = float(input("a = "))
    alpha *= sqrt(2 * pi)
    
    x, px, dpx = get_roots_Legendre(n)
    a = get_coef_Gauss_formula(x, dpx, n)
    b = get_coef_Gauss(x, n)
    
    print_table(x, a, b)
    
    res = find_limit_of_integration(0, 5, alpha, x, b)
   
    print("------------\nx = ", res)
    #print(F(res, alpha, x, b)) #NO

    '''import matplotlib.pyplot as plt
    tx = np.linspace(0, 20, 100)
    y = [F(i, alpha, x, b) for i in tx]
    plt.plot(tx, y)
    plt.show()'''

if __name__ == "__main__":
    main()

