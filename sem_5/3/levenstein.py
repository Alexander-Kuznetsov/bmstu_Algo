from time import clock

def levensteinRec(str1, str2):
    size1 = len(str1)
    if (size1 == 0):
        return len(str2)

    size2 = len(str2)
    if (size2 == 0):
        return size1

    symbIdent = 0
    if (str1[0] == str2[0]):
        symbIdent = 1

    return min((levensteinRec(str1[1:], str2) + 1),
               (levensteinRec(str1, str2[1:]) + 1),
               (levensteinRec(str1[1:], str2[1:]) + symbIdent))

def levensteinIter_3(word1, word2):
    size1, size2 = len(word1), len(word2)
    if size1 > size2:
        word1, word2 = word2, word1
        size1, size2 = size2, size1

    current_row = range(size1 + 1) 
    for i in range(1, size2 + 1):
        previous_row, current_row = current_row, [i] + [0] * size1
        for j in range(1, size1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if word1[j - 1] != word2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[size1]

def levensteinIter_4(str1, str2):
    size1, size2 = len(str1), len(str2)
    if (size1 < 2 or size2 < 2):
        return levensteinIter(str1, str2)

    if size1 > size2:
        str1, str2 = str2, str1
        size1, size2 = size2, size1
        
    prev_row = range(size1 + 1)
    curr_row = [1] + [0] * size1
    for i in range(1, size1 + 1):
        add, delete, change = prev_row[i] + 1, curr_row[i - 1] + 1, prev_row[i - 1]
        if str1[i - 1] != str2[i - 1]:
            change += 1
        curr_row[i] = min(add, delete, change)

    for i in range(2, size2 + 1):
        prev_prev_row = prev_row; prev_row = curr_row; curr_row = [i] + [0] * size1
        #prev_prev_row, prew_row, curr_row = prev_row, curr_row, [i] + [0] * size1
        add, delete, change = prev_row[1] + 1, curr_row[0] + 1, prev_row[0]
        if (str1[0] != str2[i - 1]):
            change += 1
        curr_row[1] = min(add, delete, change)

        for j in range(2, size1 + 1):
            add, delete, change, transp = prev_row[j] + 1, curr_row[j - 1] + 1, prev_row[j - 1], prev_prev_row[j - 2] + 1                                          
            if (str1[j - 1] != str2[i - 1]):
                change += 1
            curr_row[j] = min(add, delete, change, transp)

    return curr_row[size1]

def printResult(str1, str2, countOperations):
    print("Result algorithm Levenstein")
    print("With 2 words [" + str1 + ", " + str2 + "]")

    print("\nCount operations:")
    getAnswer(str1, str2)

    print("\nWork Time:")
    getWorkTime(str1, str2, countOperations)

        
def getAnswer(str1, str2):
    print("Recursion        : ", levensteinRec(str1, str2))
    print("Iterative_3 param: ", levensteinIter_3(str1, str2))
    print("Iterative_4 param: ", levensteinIter_4(str1, str2))

def getWorkTime(str1, str2, countOperations):
    timeLevensteinRec = clock()
    for i in range(countOperations):
        levensteinRec(str1, str2)
    print("Recursion        : ", '{:.9f}'.format((clock() - timeLevensteinRec)
                                                / countOperations), "second")

    timeLevensteinIter_3 = clock()
    for i in range(countOperations):
        levensteinIter_3(str1, str2)
    print("Iterative_3 param: ", '{:.9f}'.format((clock() - timeLevensteinIter_3)
                                                / countOperations), "second")

    timeLevensteinIter_4 = clock()
    for i in range(countOperations):
        levensteinIter_4(str1, str2)
    print("Iterative_4 param: ", '{:.9f}'.format((clock() - timeLevensteinIter_4)
                                                / countOperations), "second")

def main():
    countOperations = 2
    str1, str2 = "programming", "gamming"
    printResult(str1, str2, countOperations)
       
if __name__ == "__main__":
    main()
