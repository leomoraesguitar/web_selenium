# import undetected_chromedriver as uc
# from undetected_chromedriver import ChromeOptions, Chrome
# from auto_download_undetected_chromedriver import download_undetected_chromedriver


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager





from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from time import sleep
from random import uniform
from os import path, remove,environ, getenv
# from  pyperclip import copy, paste

# from  tkinter import Tk
# from webbrowser import open



class SeleniumLeo:
    def __init__(self, pprint = None, modo_oculto = False):
        self.navegador_iniciado = False
        self.p = pprint
        self.modo_oculto = modo_oculto

    def pprint(self, texto):
        if self.p != None:
            return self.p(texto)
        else:
            print(texto)

    def Tempo(self, a=0.5, b=1.0):
        tempo_aleatorio = round(uniform(a, b), 1)
        sleep(tempo_aleatorio)

    def Aguardar(self, local):
        # -> lista for vazia -> que o elemento não existe ainda
        cont = 0
        while len(self.navegador.find_elements(By.XPATH, local)) == 0:
            sleep(0.3)
            self.pprint(f'tentando localizar ({cont})')
            cont+=1
            
        self.Tempo(0.2,0.4)

    def Clicar2(self, local, t:[float, int] = None): # type: ignore
        self.Aguardar(local)
        cont = 0
        while True:
            self.Tempo(0.3,1)
            l = self.navegador.find_element(By.XPATH, local)
            if hasattr(l, 'click'):
                l.click()
                break
            self.pprint(f'tentando localizar ({cont})')
            cont+=1

        if t != None and type(t) in [float, int]:
            self.Tempo(0.1,t)

    def PesquizarXpath(self,local):
        self.Aguardar(local)
        return self.navegador.find_elements(By.XPATH, local)
    def Inserir(self, xpatch, arquivo):
        self.Aguardar(xpatch)
        self.navegador.find_element(By.XPATH, xpatch).send_keys(arquivo)

    def Enter(self, xpatch):
        self.Aguardar(xpatch)
        self.navegador.find_element(By.XPATH, xpatch).send_keys(Keys.ENTER)

    def Ctrl_letra(self, xpatch, letra):
        self.Aguardar(xpatch)
        self.navegador.find_element(
            By.XPATH, xpatch).send_keys(Keys.CONTROL, letra)
    
    def Tab(self, xpatch):
        self.Aguardar(xpatch)
        self.navegador.find_element(By.XPATH, xpatch).send_keys(Keys.TAB)
        
    def Colar(self, xpatch):
        self.Aguardar(xpatch)
        self.navegador.find_element(
            By.XPATH, xpatch).send_keys(Keys.CONTROL + "v")

    def Juntar(self, a, b):
        return path.join(a, b)

    def DefinirTamenhoPosicao(self, largura_monitor=2560, altura_monitor=1080):
        
        # Definir o tamanho da janela pela metade da largura do monitor
        # Substitua pelo tamanho do seu monitor em largura
        # Substitua pelo tamanho do seu monitor em altura
        # tamanho_janela = f"--window-size={largura_monitor//8},{altura_monitor}"
        self.navegador.set_window_size(largura_monitor//2, altura_monitor-15)
        self.navegador.set_window_position(largura_monitor//2, 0)


    # def get_screen_dimensions(self):
    #     root = Tk()
    #     root.withdraw()  # Esconde a janela principal
    #     screen_width = root.winfo_screenwidth()
    #     screen_height = root.winfo_screenheight()
    #     return screen_width, screen_height

    def verificar_pasta_perfil_chrome(self):
        user_profile = environ.get('USERPROFILE')
        if not user_profile:
            return False  # USERPROFILE não está definido

        caminho = path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Profile 1')
        if path.exists(caminho):
            return caminho
        else:
            return None


    @property
    def Iniciar(self):
        if not self.navegador_iniciado:
            options = Options()

            # perfil = self.verificar_pasta_perfil_chrome()
            # if perfil != None:
            #     options.add_argument(f'--user-data-dir={perfil}')
            # else:
            #     tutorial_criar_perfil_chrome = 'https://www.google.com/search?q=como+criar+perfil+do+chrome&sca_esv=eb02f0240770053f&sxsrf=ADLYWILKo2Dhu54HDJcAL4saWGAKBYMN9A%3A1722248903518&ei=x26nZsilH8O_5OUP35r--Ak&ved=0ahUKEwiIpe-QhcyHAxXDH7kGHV-NH58Q4dUDCBA&uact=5&oq=como+criar+perfil+do+chrome&gs_lp=Egxnd3Mtd2l6LXNlcnAiG2NvbW8gY3JpYXIgcGVyZmlsIGRvIGNocm9tZTIIECEYoAEYwwRIvxNQ6gNYsA5wAXgAkAEAmAGFAqABrgmqAQUwLjYuMbgBA8gBAPgBAZgCBKAC-APCAgoQABiwAxjWBBhHwgIKECEYoAEYwwQYCpgDAIgGAZAGCJIHAzEuM6AHtRs&sclient=gws-wiz-serp'
            #     return open(tutorial_criar_perfil_chrome)
            
            if self.modo_oculto:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                        
                # options.add_argument("--disable-gpu")

            # options.add_argument(tamanho_janela)
            # options.add_argument(f"--window-position={largura_monitor//2},0")

            # self.service = Service(ChromeDriverManager().install())    
            self.service = Service("/usr/local/bin/chromedriver") 
                   
            self.navegador = webdriver.Chrome(service=self.service, options=options)          
            self.navegador_iniciado = True
        else:
            print(f'O navegador já está iniciado')
        
        # if not self.modo_oculto:
        #     largura, altura = self.get_screen_dimensions()
        #     self.DefinirTamenhoPosicao(largura, altura)

    @property
    def FecharNavegador(self):
        if self.navegador_iniciado:
            # self.navegador.quit()
            self.navegador.close()
            self.navegador_iniciado = False


    def Abrir_site(self, link):
        if not self.navegador_iniciado:
            self.Iniciar
        if self.navegador_iniciado:
            self.navegador.get(link)