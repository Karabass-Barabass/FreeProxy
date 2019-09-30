
from intervals import *
from copy import *
import random as rnd

def setAdd(arr, a, b):    # Добавляет интервал [a, b] в множество. 
    for i in range(a, b+1):
        if i not in arr:
            arr.append(i)
    arr.sort()

def setDel(arr, a, b):     # Удаляет интервал [a, b] из множества. 
    for i in range(a, b+1):
        if i in arr:
            arr.remove(i)
    arr.sort()

def arr2Set(arr):   # Преобразует массив интервалов в числовое множество
    sett=[]
    for i in range(0, int(len(arr)/2)):
        a=arr[2*i]
        b=arr[2*i+1]
        for j in range(a, b+1):
            sett.append(j)
    return sett

# Один тест: arr1 - массив интервалов, val - интервал, op - операция
# Возвращает True при правильном выполнении.  
# При ошибке возвращает False и выводит на консоль тест для ручной отладки
def oneTest(arr1, val, op):
    arr2=arr2Set(arr1)
    arr3=deepcopy(arr1)                 # сохраняем массив
    if op.strip() == "+":               # выполняем операцию
        addValue(arr1, val)
        setAdd(arr2, val[0], val[1])
    else:
        delValue(arr1, val)
        setDel(arr2, val[0], val[1])

    arr=arr2Set(arr1)                   # сравниваем результат
    if arr2 != arr:
        lst1=array2List(arr3)
        lst2=array2List(arr1)
        print(lst1, op, val, "=", lst2, "Error", "\n")
        print('oneTest(list2Array(',lst1,'),',val,',','"',op,'")')
        return False
    else:
        lst1=array2List(arr3)
        lst2=array2List(arr1) 
        # Закомментируем чтобы не пачкать зря консоль
        #print(lst1, op, val, "=", lst2, "Ok.")
    return True

NMIN=0           # минимальное число
NMAX=10          # максимальное число
NSTEPS=10000     # число прогонов теста
# Автоматический тест
def autoTest():
    arr1=[]             # наш массив интервалов
    rnd.seed()
    for i in range(0, NSTEPS):      # прогоняем тест 1000 раз
        a=rnd.randint(NMIN, NMAX)    
        b=a
        # с вероятностью 50% выбираем число или интервал
        if rnd.randint(0, 100) > 50 :
            b=rnd.randint(NMIN, NMAX)
            if a > b :
                a, b = b, a   
        op="-"
        # с вероятностью 50% выбираем добавление либо удаление
        if rnd.randint(0, 100) > 50 :    
            op="+"
        if not oneTest(arr1, [a,b], op):
            return
    print("Done !")

autoTest() # Запускаем автоматический тест






        
    


    

    
