import requests as rqs
import base64
from PIL import Image
import numpy as np
import math
from bs4 import BeautifulSoup as soup


# Конструктор и инициализация
class ProxyRotator:
    def __init__(self):
        self.__firefox={        # Заголовки из mozilla Firefox
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",    
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "hidemy.name",
        "Referer": "https://hidemy.name/en/",        
        "Upgrade-Insecure-Requests": "1",    
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"           
        }
        self.__proxy_url="https://www.proxyrotator.com/free-proxy-list/"
        self.__digits=[]        # образцы цифр
        self.__globTab=[]       # глобальная таблица видимых стилей
        self.__countries=[]     # страны
        self.__protocols=[]     # протоколы
        self.__annons=[]        # уровни анонимности   
        self.__ports=[]         # порты
        self.__speed=0          # скорость        
        self.__loadDigits()
        
    # Грузит образцы цифр    
    def __loadDigits(self):
        for num in range(0, 10):
            img=img=Image.open("./img/"+str(num)+".png").convert('L') # грузим и преобразуем в серый без альфа
            w, h=img.size                                             # получаем размер
            a=np.array(img)                                           # в numpy
            a=a.reshape((w*h, ))                                      # преобразуем в одномерный
            a=a*1.0                                                   # преобразуем в плавающую точку
            a=a-a.sum()/(w*h)                                         # приводим среднее значение к нулю
            a=a/math.sqrt(a.dot(a))                                   # нормируем
            self.__digits.append([a, w, h])
            
            
    # Фильтрация
    
    # Чтение списков
    def getCoutriesList(self):
        return self.__countries
    def getProtocolsList(self):
        return self.__protocols
    def getAnnonsList(self):
        return self.__annons
    def getPorts(self):
        return self.__ports
    def getSpeed(self):
        
    # Получение списков имён
    def __getNames(self, lst):
        res=[]
        for item in lst:
            res.append(item[0])
        return res
    def getCountries(self):
        return self.__getNames(self.__countries)
    def getProtocols(self):
        return self.__getNames(self.__protocols)
    def getAnnons(self):
        return self.__getNames(self.__annons)
    
                   
    # Обработка ip-адреса
    
    # Разделение стилей на видимые и невидимые
    def __getVisible(self, bsObj):
        visible=["inline"]           # это всегда видимый стиль
        invisible=["none"]           # это всегда невидимый стиль
        styles=bsObj.find("style").contents[0].split("\n.")
        for i in range(1, len(styles)):
            s=styles[i]
            if 'inline' in s:
                s=s[:s.index('{')].strip()
                visible.append(s)
            else:
                s=s[:s.index('{')].strip()
                invisible.append(s)            
        return visible, invisible    
    
    # Получение ip-адреса
    def __parseIP(self, tr):
        ip=""
        vis, invis=self.__getVisible(tr)                            # видимые и невидимые стили
        syms=tr.find_all("td")[1].contents                   # получаем весь текст с мусором
        for sym in syms:
            sym=str(sym)
            if sym[0]=='<':                                  # если начинается тегом
                val=sym[sym.index('>')+1:sym.index('</')]    # вытаскиваем значение
                style=sym[sym.index('"')+1:sym.rindex('"')]  # вытаскиваем стиль
                if ':' in style:
                    style=style[style.index(':')+1:]
                # условие означает, что стиль либо локально видим, либо видим глобально и не отменен локально    
                if ((style in self.__globTab) and (not style in invis)) or (style in vis):
                    ip=ip+val
        return ip    
    
    # Получение из картинки номера порта
    def __parsePort(self, td):
        s=str(td)
        # получаем картинку
        s=s[s.index("base64,")+len("base64")+1:s.index('"/')].strip()  # получаем строку
        png=base64.b64decode(s)                                        # декодируем
        file=open("potr.png", "wb")                                    # пишем в файл
        file.write(png)
        file.close()
        # грузим картинку
        img=Image.open("potr.png").convert('L') # грузим и преобразуем в серый без альфа-канала
        W, H=img.size                           # получаем размер
        npimg=np.array(img)                     # преобразуем в numpy
        # Находим начало изображения цифр
        pos=1                                   # позиция окна сканирования
        for pos in range(1, W):    
            test=npimg[:, pos]                  # в тестовый массив вырезаем вертикальную линию
            if test.max() != test.min():        # двигаемся вперёд до тех пор, пока не встретятся 
                break                           # различные пиксели на одной вертикали
        # Начинаем собственно сканирование
        numb=""                                 # наше число
        eof=False                               # признак конца сканирования
        while (not eof):
            d=[]                                # массив оценок для каждой цифры
            e=[]                                # массив смещений для каждой цифры
            eof=True
            for i in range(0, 10):              # проходим по каждой цифре
                dd=[]                           # массив оценок для цифры при смещении окна
                ww=self.__digits[i][1]          # ширина цифры
                hh=self.__digits[i][2]          # высота цифры
                for j in range(-1, 2):          # пробуем каждую цифру при смещениях окна -1, 0, 1
                    if pos+j+ww < W:            # проверяем, впишется ли цифра в остаток картинки по ширине
                        eof=False
                        test=npimg[:,pos+j:pos+j+ww] # вырезаем с позиции+смещение окно шириной ww
                        tt=test.copy()               # копируем, чтобы не затирать изображение
                        tt=tt.reshape((ww*hh, ))     # преобразуем в одномерный массив
                        tt=tt*1.0                    # преобразуем в плавающую точку
                        tt=tt-tt.sum()/(ww*hh)       # приводим среднее значение к нулю
                        tt=tt/math.sqrt(tt.dot(tt))  # нормируем
                        prod=tt.dot(self.__digits[i][0])    # вычисляем оценку - скалярное произведение
                        dd.append(prod)              # сохраняем оценку
                if not eof:
                    m=max(dd)                   # максимальная оценка при различных смещениях
                    im=dd.index(m)              # смещение окна для этой оценки (начинается с -1)
                    d.append(m)                 # сохраняем оценку и смещение
                    e.append(im-1)
            # выбираем цифру с наивысшей оценкой
            if not eof:
                m=max(d)
                im=d.index(m)
                s=e[im]
                if m > 0.9:                # если оценка велика, дописываем соответствующую цифру
                    numb=numb+str(im)
                    pos+=self.__digits[im][1]+s   # и продвигаем позицию окна на ширину цифры
                else:                      
                    pos+=1                 # если оценка недостаточна, сдвигаем окно на 1
        return numb        
    
    # Всё остальное
    
    # Парсит скорость
    def __parseSpeed(self, td):
        ii=td.find_all("i")
        s=len(ii)
        for i in ii:
            if i.attrs["class"][1] == "fa-star-o" :
                s-=1
        return s
            
    # Парсит страну
    def __parseCountry(self, td):
        s=td.contents[1].strip()
        if "," in s:
            s=s.split(",")[1].strip()
        return s
        
    # Парсит строку таблицы
    def __parseTR(self, tr):
        result=[]
        tds=tr.find_all("td")
        result.append(self.__parseIP(tr))                       # получаем ip-адрес
        result.append(self.__parsePort(tds[2]))                 # получаем номер порта
        result.append(self.__parseCountry(tds[3]))              # получаем страну
        result.append(self.__parseSpeed(tds[4]))                # получаем скорость
        result.append(tds[5].contents[0].strip())               # получаем протокол
        result.append(tds[6].contents[0].strip())               # получаем уровень анонимности
        return result
        
        
    # Фильтр - пока ничего не делает, просто заглушка
    def __filtr(self, proxy):
        #return [proxy[0], proxy[1]]
        return proxy
    
    # Чтение странички с proxyrotator
    def readPage(self, page):
        result=[]
        if page < 1:     # страницы там от 1 до 10
            page=1
        if page > 10:
            page=10
        rsp=rqs.get(self.__proxy_url+str(page)+'/', headers=self.__firefox)         
        html=str(rsp.content.decode(rsp.encoding))                      
        
        # При желании сохраняем файл для контроля
        file=open("proxyrotator.html", "wt")               
        file.write(html)
        file.close()
         
        bsObj=soup(html, "lxml")                          # создаём объект для парсера
        self.__globTab, invis=self.__getVisible(bsObj)    # получаем глобальную таблицу видимых стилей
        table=bsObj.find("tbody")                         # таблица прокси
        trs=table.find_all("tr")                          # список строк
        for tr in trs:
            r=self.__filtr(self.__parseTR(tr))            # парсим все строки, фильтруя результат
            if r != None:
                result.append(r)                          # сохраняем, если результат прошел фильтр 
        return result
    
rot=ProxyRotator()
res=rot.readPage(1)
print(res)
        
        
"""
[['41.204.84.182',  '53281', 'Cameroon',      3, 'HTTP(S)', 'Elite'], 
['120.83.103.250',  '9999',  'China',         4, 'HTTP(S)', 'Elite'], 
['80.73.90.18',     '3128',  'Russia',        4, 'HTTP(S)', 'Elite'], 
['1.199.193.207',   '9999',  'China',         4, 'HTTP(S)', 'Elite'], 
['31.41.92.154',    '23500', 'Ukraine',       4, 'HTTP(S)', 'Elite'], 
['5.10.90.214',     '8080',  'Netherlands',   4, 'HTTP(S)', 'Elite'], 
['205.201.202.67',  '48469', 'United States', 4, 'HTTP(S)', 'Elite'], 
['190.152.245.18',  '8080',  'Ecuador',       4, 'HTTP(S)', 'Elite'], 
['103.209.89.69',   '8080',  'India',         4, 'HTTP(S)', 'Elite'], 
['185.231.209.233', '41258', 'Italy',         4, 'HTTP(S)', 'Elite'], 
['103.209.89.67',   '8080',  'India',         4, 'HTTP(S)', 'Elite'], 
['45.6.92.38',      '8080',  'Brazil',        4, 'HTTP(S)', 'Elite'], 
['101.109.33.225',  '8080',  'Thailand',      4, 'HTTP(S)', 'Elite'], 
['83.147.240.127',  '8080',  'Iran',          4, 'HTTP(S)', 'Elite'], 
['109.200.155.197', '8080',  'Ukraine',       4, 'HTTP(S)', 'Elite'], 
['213.163.122.196', '8080',  'Albania',       4, 'HTTP(S)', 'Elite'], 
['43.250.81.142',   '8080',  'Bangladesh',    4, 'HTTP(S)', 'Elite'], 
['179.164.215.44',  '8080',  'Brazil',        3, 'HTTP(S)', 'Elite'], 
['83.12.5.154',     '8080',  'Poland',        4, 'HTTP(S)', 'Elite'], 
['191.241.36.170',  '8080',  'Brazil',        4, 'HTTP(S)', 'Elite'], 
['134.35.58.104',   '8080',  'Yemen',         2, 'HTTP(S)', 'Elite'], 
['213.58.202.70',   '54214', 'Portugal',      4, 'HTTP(S)', 'Elite'], 
['134.35.194.26',   '8080',  'Yemen',         4, 'HTTP(S)', 'Elite'], 
['188.94.231.69',   '8080',  'Russia',        3, 'HTTP(S)', 'Elite'], 
['123.115.112.29',  '9000',  'China',         4, 'HTTP(S)', 'Elite']]

"""