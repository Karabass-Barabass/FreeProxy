"""
Это общий класс для HidemyName и ProxyRotator. Сюда скинута вся не особо интересная возня с различными
списками настроек фильтрации. Если нет желания, этот код можно не смотреть. Для понимания работы скрапперов
он не даёт ровным счетом ничего. Тем не менее немного объясню что тут делается.

Фильтры стран, протоколов и уровней анонимности построены единообразно, как списки свойств. Сами свойства 
тоже является списками, содержащим как минимум имя свойства, его состояние ("yes" - разрешено или "no" - запрещено),
плюс возможно что-то ещё (например код страны). Соответственными будут и их методы
- Включить свойство
- Выключить свойство
- Включить все
- Выключить все
- Получить весь список свойств
- Получить имена свойств

Фильтр портов немудряще построен по образцу hidemy.name, как список либо чисел - разрешенных портов, либо 
интервалов вида [число_от - число_до]. Только для hidemy.name он используется при формировании запроса, а для
proxyrotator.com - для последующей фильтрации. Его операции:
- Добавить число или интервал
- Удалить число или интервал
- Читать список
Тут применяются довольно нетривиальные действия со списками интервалов, что вынесенно в отдельный файл (плюс тесты),
и даже удостоилось статьи на хабре в качестве задачки с изюминкой. 

Ну и наконец. Скорость. Тут всё просто. Её можно только задавать и читать.
Вот примерно так. Ну что же, поехали !
"""


class ProxyFilter:
    def __init__(self):
        self.__countries=[]                  # страны
        self.__protocols=[]                  # протоколы
        self.__annons=[]                     # уровни анонимности
        self.__ports=[]                       # порты
        self.__speed=0                       # скорость
    
    # Получение списков. Тут всё ясно
    def getCoutriesList(self):
        return self.__countries
    def getProtocolsList(self):
        return self.__protocols
    def getAnnonsList(self):
        return self.__annons
    def getPorts(self):
        return self.__ports
    def getSpeed(self):
        return self.__speed
    def setSpeed(self, speed):
        self.__speed=speed
        
    # получение имён свойств    
    def __getNames(self, lst):
        res=[]
        for item in lst:
            res.append(item[0])  
            
    def getCountries(self):
        return self.__getNames(self.__countries)
    def getProtocols(self):
        return self.__getNames(self.__protocols)
    def getAnnons(self):
        return self.__getNames(self.__annons)
    
    # Операции со списками свойств
    def __changeList(self, lst, param, y):
        if type(param) != list:
            param=[param]
        for item in param:
            for name in lst:
                if name[0]==item:
                    name[2]=y
                    
    def __allList(self, lst, y):
        for name in lst:
            name[2]=y;
    
    def addCountry(self, country):
        self.__changeList(self.__countries, country, "yes")
    def delCountry(self, country):
        self.__changeList(self.__countries, country, "no")
    def allCountry(self):
        self.__allList(self.__countries, "yes")
    def clearCountry(self):
        self.__allList(self.__countries, "no")
        
    def addProtocol(self, protocol):
        self.__changeList(self.__protocols, protocol, "yes")
    def delProtocol(self, protocol):
        self.__changeList(self.__protocols, protocol, "no")
    def allProtocol(self):
        self.__allList(self.__protocols, "yes")
    def clearProtocol(self):
        self.__allList(self.__protocols, "no")
        
    def addAnnon(self, annon):
        self.__changeList(self.__annons, annon, "yes")
    def delAnnon(self, annon):
        self.__changeList(self.__annons, annon, "no")
    def allAnnon(self):
        self.__allList(self.__annons, "yes")
    def clearAnnon(self):
        self.__allList(self.__annons, "no")


        





            
            
        
        
        
        
 
        
            
                
                
        
        
    
    
    
            
    
        
    
    