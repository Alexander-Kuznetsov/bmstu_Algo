from time import clock
from random import *

def BubbleSort(arr):
    for i in range(len(arr)):
        swap = False
        for j in range(len(arr) - (i + 1)):
            if (arr[j + 1] < arr[j]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap = True
        if (not swap):
            break

def InsertSort(arr):
    for i in range(1, len(arr)):
        while (i > 0 and arr[i] < arr[i - 1]):
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1

def SelectSort(arr):
    for i in range(len(arr) - 1):
        j = arr[i:].index(min(arr[i:]))
        arr[i], arr[j + i] = arr[j + i], arr[i]


def createSortArr(size):
    return [i for i in range(size)]
     
def createRevSortArr(size):
    return [i for i in reversed(range(size))]

def createRandArr(size):
    arr = []
    for i in range(size):
        arr.append(randint(0, size - 1))
    return arr
    
def timeTest(iterations, arr_size, sort):
    timeSort = 0; timeRev = 0; timeRand = 0
    for i in range(iterations):
        arr = createSortArr(arr_size)
        time = clock()
        sort(arr)
        timeSort += (clock() - time)

        arr = createRevSortArr(arr_size)
        time = clock()
        sort(arr)
        timeRev += (clock() - time) 

        arr = createRandArr(arr_size)
        time = clock()
        sort(arr)
        timeRand += (clock() - time)
    
    print("Best time  : ",  '{:.9f}'.format(timeSort / iterations))
    print("Worst time : ",  '{:.9f}'.format(timeRev / iterations))
    print("Random time: ",  '{:.9f}'.format(timeRand / iterations))
    
def getTest(size, iterations):
    for i in range(len(size)):
        print(size[i], " elements")
        print("Insert Sort")
        timeTest(iterations, size[i], InsertSort)
        print("Selection Sort")
        timeTest(iterations, size[i], SelectSort)
        print("Bubble Sort")
        timeTest(iterations, size[i], InsertSort)
        print()
        

def main():
    size = [10, 100, 1000, 5000]
    iterations = 5
    
    getTest(size, iterations)

if __name__ == "__main__":
    main()
