import math

def func(x, y):
    return math.exp(x**3 - y) - x**6 + 2 * x**3 * y + 2 * x**3 - y**2 - 2 * y - 2

def main():
    a = 0      		#Нижняя граница
    b = 2	   	#Верхняя граница
    eps = 1e-5 		#Погрешность
    I = 0               #Значение интеграла
    n = 50      	#Количество разбиений
    I = calculate_integral(a, b, n, eps)

    print("From ", a, " to ", b, "\nResult: ", round(I, 5))

def calculate_integral(A, B, n, eps):
    a = b = A      	         #Новая нижняя граница && Новая верхняя граница
    step = abs((B - A) / n)      #Шаг
    S = 0
    a_root = calculate_root(a, eps) / 2
    while (b <= B):         
            b += step
            b_root = calculate_root(b, eps) / 2
            S += (a_root + b_root) 
            a_root = b_root
    return S * step

def calculate_root(x, eps):
    a, b = -100, 100
    return (half_interval_root(func, a, b, eps, x))  

def half_interval_root(f, a, b, eps, x):  #Метод половинного деления
    fa = func(x, a)
    fb = func(x, b) 
    if fa == 0: return a
    if fb == 0: return b
    if fa * fb < 0:
        c = (a + b) / 2
        while abs(b - a) > abs(c) * eps + eps:
            c = (a + b) / 2
            fc = func(x, c)
            if fa * fc < 0:
                b = c
            else:
                a = c
        return c
    return 0

if __name__ == "__main__":
	main()
