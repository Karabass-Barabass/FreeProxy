import requests as rqs
import time
from bs4 import BeautifulSoup as soup
import subprocess
from proxyfilter import ProxyFilter 

class HidemyName(ProxyFilter):

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
        self.__cookies={}       # куки
        self.__html=""          # код странички
        self.__proxy_url="https://hidemy.name/en/proxy-list/"  # список прокси
        self.__hidemyname="https://hidemy.name"                # корневой url
        self.__hostname="hidemy.name"                          # имя сайта
        self.__nodename="node"                                 # под Windows возможно node.exe

    # Чтение внутренних переменных    
    def getCookies(self):
        return self.__cookies
    def getHtml(self):
        return self.__html
    
            
    # Подключение
    def __getScript(self, html):
        try:
            script="var "
            s=html[html.index("setTimeout"):]
            a=s.split("=")
            name=a[0][a[0].rfind(",")+1:].strip()
            script=script+name+"="
            a1=a[1].split('"')
            name=name+"."+a1[1]
            script=script+a[1]
            script=script[:script.index(";")+1]+"\n"
            script=script+html[html.index(name):]
            script=script[:script.index("value")]
            script=script[:script.rindex(";")+1]+"\n"
            script=script+'var t="'+self.__hostname+'";\n'
            script=script+"var a=("+name+"+t.length).toFixed(10);\n"
            script=script+"console.log(a);\n"
            return script
        except ValueError :
            return None    
    
    def getControls(self):
        bsObj=soup(self.__html, "html.parser") 
        countries=[]
        protocols=[]
        annons=[]
        labels=bsObj.find_all("label")                      
        for i in range(0, len(labels)):
            label=labels[i]
            inp=label.find("input")
            if "class" in inp.attrs.keys():
                cls=inp.attrs["class"]
                if "choose-country" in cls :
                    name=label.contents[4].contents[0]
                    name=name[:name.index("(")].strip()
                    code=inp.attrs["id"]
                    code=code[code.rindex("_")+1:]
                    countries.append([name, code, "yes"])    
            elif "id" in inp.attrs.keys():
                if inp.attrs["id"][0]=="t":
                    name=label.contents[2].contents[0]
                    code=inp.attrs["id"][2:]
                    protocols.append([name, code, "yes"])
                elif inp.attrs["id"][0]=="a":
                    name=label.contents[2].contents[0]
                    code=inp.attrs["id"][2:]
                    annons.append([name, code, "yes"])    
        self.__countries=countries 
        self.__protocols=protocols
        self.__annons=annons
    
    def connect(self):
        try:
            self.__cookies={}
            error="rq1"
            rsp=rqs.get(self.__proxy_url, headers=self.__firefox)      # читаем страничку
            error="script"
            html=str(rsp.content.decode(rsp.encoding))    
            script=self.__getScript(html)                        # получаем и записываем скрипт
            if script==None:
                return None
            file=open("script.js", "wt")                       
            file.write(script)
            file.close()
            cc=rsp.cookies.get_dict()                    # получаем и сохраняем куку
            self.__cookies.update(cc)
            error="exec"
            s=subprocess.Popen(self.__nodename+" script.js", shell=True, stdout=subprocess.PIPE) # выполняем скрипт
            s=s.stdout.read().decode("utf-8")                                             # получаем результат 
            # Обработка формы
            error="form"
            param={}       
            # словарь для параметров
            bsObj=soup(html, "lxml")                     # создаем объект BeautifulSoup
            form=bsObj.find("form")                      # находим форму
            inputs=form.find_all("input")                # находим в форме все теги input
            for i in range(0, len(inputs)):              # проходимся по всему найденному списку  
                name=inputs[i].attrs["name"]             # получаем атрибут name
                if name=="jschl_answer":                 # если имя jschl_answer, подсовываем туда результат скрипта
                    value=s.strip()                      # обрезаем \n на конце
                else:
                    value=inputs[i].attrs["value"]       # получаем атрибут value из формы
                param[name]=value                        # скидываем в список параметров
            action=form.attrs["action"]                  # получаем атрибут формы action
            url=self.__hidemyname+action                 # по этому адресу и надо посылать ответ
            # Отправляем проверочный ответ
            error="wait"
            time.sleep(4)                                # ждем 4 секунды
            rsp=rqs.get(url, headers=self.__firefox, cookies=self.__cookies, params=param)     # отправляем запрос
            error="rq2"
            html=str(rsp.content.decode(rsp.encoding))
            rsp=rsp.history[0]
            cc=rsp.cookies.get_dict()                    # получаем и сохраняем куку
            self.__cookies.update(cc)
            self.__html=html
            error="ok"
            if len(self.__countries)==0:    
                error="parse"
                self.getControls()
                error="ok"
            return error
        except:
            return error
        
    # Штатное чтение
    def __lookupList(self, lst):
        res=""
        n=0
        for item in lst:
            if lst[2]=="yes":
                res=res+item[1]
                n=n+1
        if n==len(lst):
            res=""
        return res
    
    def __makeParams(self):
        con=self.__lookupList(self.__countries)
        ptk=self.__lookupList(self.__protocols)
        ann=self.__lookupList(self.__annons)
        prt=""
        for p in self.__ports:
            prt=prt+p+","
        prt=prt[:prt.rindex(",")]
        return con, ptk, ann, prt
    
    def read(self, page):
        con, ptk, ann, prt=self.__makeParams()
        
        
        
        
hidemy=HidemyName()
hidemy.connect()

    
