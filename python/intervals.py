
# Работа с интервалами. Подробные комментарии к этому довольно нетривиальному коду в статье на хабре.

# Первым делом преобразуем удобный для восприятия формат списка в массив, и обратно
def list2Array(lst):  # преобразует список в массив
    arr=[]            
    for i in range(0, len(lst)):
        if type(lst[i])==list:
            arr.append(lst[i][0])
            arr.append(lst[i][1])
        else:
            arr.append(lst[i])
            arr.append(lst[i])
    arr.sort()
    return arr
            
def array2List(arr):  # преобразует массив в список
    lst=[]
    for i in range(0, int(len(arr)/2)):
        if arr[2*i]!=arr[2*i+1]:
            lst.append([arr[2*i], arr[2*i+1]])
        else:
            lst.append(arr[2*i])
    return lst


# Ищет в массиве arr интервалы, близкие к интервалу s. 
# Возвращает массив их индексов
# При d=0 ищутся пересекающиеся интервалы. 
# При d=1 - пересекающиеся и непосредственно примыкающие
def findNear(arr, s, d):
    idx=[]
    for i in range(0, (int)(len(arr)/2)):
        a=arr[2*i]; b=arr[2*i+1]; p=s[0]-d; q=s[1]+d; j=2*i;
        if (a >= p) and (a <= q):
            idx.append(j)
        if (b >= p) and (b <= q):
            if not j in idx:
                idx.append(j)
        if not j in idx:
            if (p >= a) and (p <= b):
                idx.append(j)
            if (q >= a) and (q <= b):
                if not j in idx:
                    idx.append(j)
    return idx



# Сумма интервалов, представленных парами чисел
# Просто интервал от самого левого до самого правого из концов слагаемых
def itvlSum(lst):  
    left=[]        # массив левых концов
    right=[]       # массив правых концов
    for i in range(0, (int)(len(lst)/2)):
        left.append(lst[2*i])
        right.append(lst[2*i+1])
    return [min(left), max(right)]

# Разность интервалов двух
# Интервал two как бы пытается вырезать дырку в one
def itvlDiff(one, two):
    diff=[]             # наша разность
    left=two[1]+1       # левая граница разности
    right=two[0]-1      # правая граница разности
    if one[0] <= right:
        diff.append(one[0])  # левый интервал разности
        diff.append(right)
    if one[1] >= left:
        diff.append(left)    # правый интервал разности
        diff.append(one[1])
    return diff

# Добавить число или интервал
def addValue(arr, val):
    if type(val) != list:   # преобразуем в интервал 
        val=[val, val]
    if val[0] > val[1]:
        val=[val[1], val[0]]    # сортируем
        
    idx=findNear(arr, val, 1)   # находим соприкасающиеся
    s=[]                        # добавляемый список
    if len(idx) == 0: 
        s=val                   # случай 1
    elif len(idx) == 1:         # случай 2
        s=itvlSum([arr[idx[0]],arr[idx[0]+1],val[0],val[1]])
    elif len(idx) > 1:          # случаи 3 и 4
        ss=[arr[idx[0]],arr[idx[0]+1]]
        ss+=arr[idx[-1]],arr[idx[-1]+1]
        ss+=[val[0],val[1]]
        s=itvlSum(ss)
    if len(idx) != 0:    
        del arr[idx[0]:idx[-1]+2]   # удаляем всё, что пришло в idx
    arr+=s                          # добавляем s
    arr.sort()                      # пересортировываем
    
def delValue(arr, val):    
    if type(val) != list:   # преобразуем в интервал 
        val=[val, val]
    if val[0] > val[1]:
        val=[val[1], val[0]]    #  сортируем
    
    idx=findNear(arr, val, 0)   # находим пересекающиеся
    if len(idx) == 0:
        return                  # случай 1
    s=itvlDiff([arr[idx[0]], arr[idx[0]+1]], [val[0], val[1]])
    if len(idx) > 1:            # случаи 3 и 4
        s=s+itvlDiff([arr[idx[-1]], arr[idx[-1]+1]], [val[0], val[1]])
    if len(idx) != 0:    
        del arr[idx[0]:idx[-1]+2]   # удаляем абсолютно всё, что пришло в idx
    arr+=s                          # добавляем s
    arr.sort()                      # пересортировываем
    