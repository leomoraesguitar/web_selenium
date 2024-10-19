
import flet as ft
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from  tkinter import Tk
from selenium_leo1 import SeleniumLeo, By
from re import findall, sub, search
# import pickle
import os
from time import sleep
# import pandas as pd
from dotenv import load_dotenv


load_dotenv()
# Acessa a variável de ambiente



class ClassName(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.navegador_iniciado = False
        self.selenium = SeleniumLeo(print, modo_oculto=True)
        # self.pprint = print
        self.nometabela = 'tabela.plk'
        self.login_tj = False

        self.usuario = os.getenv("USUARIO")
        self.senha = os.getenv("SENHA")


        self.home = '//*[@id="menuPrincipal"]/ul/li[1]/a/span'
        self.cem = '//*[@id="mov:j_id2"]/option[3]'
        self.campo_login = '//*[@id="loginName"]'
        self.campo_senha = '//*[@id="loginSenha"]'
        self.btn_entrar = '//*[@id="btnEntrar"]/span[2]'
        self.quantidade_de_mandados = '//*[@id="gridAtividades:0:quantidade"]'
        self.proxima_pagina = '//*[@id="mov_paginator_top"]/a[3]'


        self.saida = ft.Text('')

        self.controls = [
            ft.FilledButton(
                text = 'raspar',
                on_click=self.Atualizar_tabela_picle,
            ),
            ft.ListView([self.saida], expand=True, auto_scroll=True)
        ]


    def pprint(self, *texto):
        for i in list(texto):
            self.saida.value += f'{i}\n'
            self.saida.update()


    def Abrir(self, e):
        link = "https://www.tjse.jus.br/oficialjustica/paginas/movimentacaoMandado/movimentacaoMandado.tjse"

        # self.driver = webdriver.Chrome(service=self.service, options=options)

        # self.driver.get(link)]
        self.Abrir_site(link)

        while True:
            sleep(120)      


    def FazerLoginTJ(self):
        link = "https://www.tjse.jus.br/oficialjustica/paginas/movimentacaoMandado/movimentacaoMandado.tjse"
        self.pprint('Abrindo Portal do Oficial...')
        def entrar():
            self.selenium.Abrir_site(link)
            # self.selenium.Aguardar = self.Aguardar2
            clic_login = '//*[@id="menuPrincipal"]/ul/li/a/span'
            entrar = '//*[@id="btnEntrar"]/span[2]'
            número_de_mandado = '//select[@id="mov:j_id2"]'
            # cem = '//*[@id="mov:j_id2"]/option[3]'
            # time.sleep(5)
            def Login():
                self.selenium.Clicar2(clic_login)
                self.selenium.Inserir(self.campo_login, self.usuario)
                self.selenium.Inserir(self.campo_senha, self.senha)
                self.selenium.Clicar2(self.btn_entrar)

                sleep(1)
                if len(self.selenium.navegador.find_elements(By.XPATH, self.cem)) == 0:
                    self.selenium.Clicar2(entrar)
                    sleep(1)

            # th = Thread(target=Login, daemon=True)
            # th.start()
            # sleep(30)
            # th.join()
            self.pprint('Fazendo login...')                
            Login()
            self.pprint('Login realizado com sucesso!')

            self.login_tj = True
        
        try:
            entrar()
        except:
            entrar()


    def VerificarNavegadorAberto(self):
        if not self.selenium.navegador_iniciado:
            self.pprint('Abrindo Navegador...')
            self.selenium.Iniciar

        if self.selenium.navegador_iniciado:
            self.pprint('Navegador abterto com sucesso!')

            if not self.login_tj:
                self.FazerLoginTJ()
                sleep(1)
            self.pprint('Raspando mandados...')
        


    def Atualizar_tabela_picle(self,e):
        # self.SalvarPickle(self.tabela, self.nometabela_backup)

        def Texto(xpatch):
            return self.selenium.navegador.find_element(By.XPATH, xpatch).text

        def LocalizaIndex(df,coluna, valor):
            return  df.index[df[coluna] == valor].tolist()[0]    

        self.VerificarNavegadorAberto()

        self.selenium.Clicar2(self.home)
        try:
            self.selenium.Clicar2(self.cem)
        except:
            pass        
        sleep(5)

        # self.GerarListaMandadosAntigos()

        self.mandados_antigos = []
        self.mandados_antigos_index = []
        if os.path.exists(self.nometabela):
            # self.tabela = self.LerPickle(self.nometabela)
            self.tabela = None
            if not self.tabela is None:
                self.mandados_antigos = list(self.tabela.get('Nº do mandado:', [])) 
            else:
                self.mandados_antigos = []

        



        # try:
        # self.selenium.Aguardar('//*[@id="mov_data"]/tr['+f'{1}]/td[2]/a[1]')   



        colunas = ['Nº do Processo:', 'Nº do mandado:', 'Destinatario do mandado:','Endereco', 'Situação','Prioridade','Audiência','Recebimento', 'Final de prazo','ação', 'Tipo do mandado:', 'Audiência',  'telefone']
        self.dic_cols_tabela2 = {i:[] for i in colunas}

        self.cont = 0

        total_de_mandados = int(self.selenium.navegador.find_element(By.XPATH, self.quantidade_de_mandados).text) 
        self.pprint('total de mandaos no site: ', total_de_mandados)
        novos_manadados = 0
        # from IPython.display import clear_output


        while True:            
            tabelageral = '//*[@id="mov_data"]'
            t = self.selenium.navegador.find_element(By.XPATH, tabelageral)
            if hasattr(t, 'text'):
                texto = t.text
                mandados = [i.strip() for i in findall(r'\b\n\d{12}\n', texto)]

                index_para_raspar = []
                for num_mandado in mandados:
                    if num_mandado not in self.mandados_antigos:
                        id = mandados.index(num_mandado) +1
                        index_para_raspar.append(id)

                    else:   
                        if isinstance(self.tabela, pd.DataFrame):            
                            indice = LocalizaIndex(self.tabela,'Nº do mandado:',num_mandado)
                            # self.pprint(f"O mandado {num_mandado} - {self.tabela.loc[indice,'Destinatario do mandado:']} já estava na planilha")
                            self.mandados_antigos_index.append(indice)

                    self.cont +=1

                if len(index_para_raspar)>0:
                    for i in index_para_raspar:
                        xpathes_dic = {
                        'Nº do mandado:':'//*[@id="mov_data"]/tr['+f'{i}]/td[3]/div/a[1]',
                        'Nº do Processo:':'//*[@id="mov_data"]/tr['+f'{i}]/td[2]/a[1]',
                        'Destinatario do mandado:':'//*[@id="mov_data"]/tr['f'{i}]/td[4]/div/span',
                        'Endereco':'//*[@id="mov_data"]/tr['+f'{i}]/td[5]/div/span',
                        'Situação':'//*[@id="mov_data"]/tr['+f'{i}]/td[6]',
                        'Prioridade':'//*[@id="mov_data"]/tr['+f'{i}]/td[7]/div/span',
                        'Audiência':'//*[@id="mov_data"]/tr['+f'{i}]/td[8]/span',
                        'Recebimento':'//*[@id="mov_data"]/tr['+f'{i}]/td[9]/span',
                        'Final de prazo':'//*[@id="mov_data"]/tr['+f'{i}]/td[10]/span'
                        }        

                        num_mandado = Texto(xpathes_dic['Nº do mandado:'])
                        # print('num mandado:',num_mandado )


                        self.pprint(f'lendo  o mandado {num_mandado} ...')
                        for i in self.dic_cols_tabela2.keys():
                            try:
                                self.dic_cols_tabela2[i].append(Texto(xpathes_dic[i]))
                            except:
                                self.dic_cols_tabela2[i].append('')
                        novos_manadados +=1  
                
            else:
                self.pprint(f'verifique o xpath "{tabelageral}"')

            if len(self.selenium.navegador.find_elements(By.XPATH, self.proxima_pagina)) > 0 and self.cont  < total_de_mandados:
                self.pprint('Raspando a página seguinte')
                self.selenium.Clicar2(self.proxima_pagina)
                sleep(5)
            else:
                break
        # clear_output()    
        self.pprint(f'Foram encontrados {novos_manadados} novos mandados')
        self.pprint('Todos os mandaos foram raspados')


        df_novos = None
        df_antigos = None
        self.pprint(self.dic_cols_tabela2)
        # if len(self.dic_cols_tabela2['Nº do mandado:']) > 0:
        #     m = MandadoReduzido(
        #         dic_cols_tabela2_para_extracao = self.dic_cols_tabela2, 
        #         caminho = self.pasta_mandados,
        #         dic_contatosjson = self.contatos_na_agenda,
        #         pprint = self.pprint,
        #     )
        #     m.ExtrairDadosMandadosTJSE()
        #     df_novos = DataFrame(m.dic)

        # if hasattr(self,'tabela' ) and isinstance(self.tabela,DataFrame):
        #     if list(self.tabela.columns) == self.colunas_padrao_tabela and self.tabela.shape[0] > 0:
        #         if len(self.mandados_antigos_index) > 0:# and len(self.mandados_antigos_index) != self.tabela.shape[0]
        #             dic_antigos = self.tabela.iloc[self.mandados_antigos_index,:].to_dict(orient='list')
        #             df_antigos = DataFrame(dic_antigos)


        # if  not df_antigos is None and  not df_novos is None:          
        #     df2 = concat([df_antigos, df_novos], axis = 0)  
        # elif not df_antigos is None:
        #     df2 = df_antigos
        # elif not df_novos is None:
        #     df2 = df_novos



        # if not df_antigos is None or not df_novos is None:   
        #     self.tabela = df2.sort_values(by='ação')
        #     self.tabela.reset_index(drop = True, inplace=True)
        #     if self.atualizar_plan_externa:
        #         self.Inserir_tabela_na_planilha(self.tabela)

        #     self.Adicionar_zap_a_tabela()

        #     self.Savar_tabela()

        #     if hasattr(self, 'colunas_viziveis'):
        #         self.GeraLinha()
        #         # tabela2 = TabelaMandadosAcoes(self.tabela.loc[:,self.linha], self.Enviar_um_mandado, height = self.height-60)        
        #         tabela2 = ResponsiveTablle(self.tabela.loc[:,self.linha], self.Enviar_um_mandado)        
        #         self.Exibir_tabela(tabela2)
        #     try:
        #         self.update()
        #         self.pprint('Planilha interna atualizada com sucesso!')
        #     except:
        #         pass


    # def SalvarPickle(self, var, nome):
    #     if not nome.endswith('.plk'):
    #         nome += '.plk'        
    #     with open(nome, 'wb') as arquivo:
    #         pickle.dump(var, arquivo)

    # def LerPickle(self, nome):
    #     if not nome.endswith('.plk'):
    #         nome += '.plk'
    #     if os.path.isfile(nome):
    #         with open(nome, 'rb') as arquivo:
    #             return pickle.load(arquivo)
    #     else:
    #         return None    




def main(page: ft.Page):
    # Definindo o t�tulo da p�gina
    page.title = 'Título'
    page.window.width = 500  # Define a largura da janela como 800 pixels
    page.window.height = 385  # 
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        scrollbar_theme = ft.ScrollbarTheme(
            thickness = {
                ft.ControlState.HOVERED:20,
                ft.ControlState.DRAGGED:20, 
                ft.ControlState.SCROLLED_UNDER:20
                  },
        ),
        use_material3 = True,
        color_scheme=ft.ColorScheme(
            primary = ft.colors.WHITE70, # fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone, texto, texto do elevatebuton
            on_primary = ft.colors.BLACK, #cor texto filledbutton e cor da bolinha do swicth com True
            secondary_container = ft.colors.GREY_700, # cor de fundo filledtonalbutton
            on_secondary_container = ft.colors.WHITE, # cor de texto filledtonalbutton
            outline = ft.colors.GREY_600, #cor de borda do outliedbutton
            shadow = ft.colors.BLUE_300, # cor das sombras
            on_surface_variant = ft.colors.WHITE, #cor dos labels, cor da caixa do checkbox e cor do check do popmenubutton
            surface_variant = ft.colors.GREY_600, #cor do slider e cor de fundo do texfield e do dropbox
            primary_container = ft.colors.WHITE70, #cor HOVERED da bolinha do switch
            on_surface = ft.colors.WHITE, #cor HOVERED do checkbox e cor dos items do popmenubuton

        ),
        divider_theme=ft.DividerTheme(
            color=ft.colors.with_opacity(0.5, ft.colors.GREY_800),      # Cor do divisor
            thickness=1,               # Espessura da linha divisória
            leading_indent=1,                 # Recuo inicial
            trailing_indent=1              # Recuo final
        ),
        text_theme=ft .TextTheme(
            title_large=ft.TextStyle(
                size = 20,
                weight=ft.FontWeight.W_800,
            )
        ),
        slider_theme=ft.SliderTheme(
            thumb_color = ft.colors.GREY_700,
        ),
        switch_theme= ft.SwitchTheme(
            thumb_color = {
                ft.ControlState.DEFAULT:ft.colors.GREY_400,
                ft.ControlState.HOVERED:None,
                ft.ControlState.SELECTED:ft.colors.GREY_300,

            },
            track_color = {
                ft.ControlState.DEFAULT:ft.colors.GREY_700,
                ft.ControlState.HOVERED:ft.colors.GREY_700,
            },
            overlay_color = {
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            },
            track_outline_color= {
                ft.ControlState.DEFAULT:ft.colors.WHITE,
                ft.ControlState.HOVERED:ft.colors.WHITE,
            },
            track_outline_width= {
                ft.ControlState.DEFAULT:0,
                ft.ControlState.HOVERED:0
            },
        ),
        checkbox_theme = ft.CheckboxTheme(
            overlay_color = {
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            },                
        ),
    )


    page.navigation_bar = ft.CupertinoNavigationBar(
    bgcolor= ft.colors.BLACK38,
    inactive_color=ft.colors.GREY,
    active_color=ft.colors.GREEN_800,
    on_change=lambda e: print('Selected tab:', e.control.selected_index),
    destinations=[
        ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label='Explore'),
        ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label='Commute'),
        ft.NavigationBarDestination(
            icon=ft.icons.BOOKMARK_BORDER,
            selected_icon=ft.icons.BOOKMARK,
            label='Explore',
        ),
    ]
    )
    
    page.appbar = ft.AppBar(
    actions = [],
    title=ft.Text(
        value = 'Barrade Navegação superior', 
        weight='BOLD', 
        color=ft.colors.GREEN_600,
        style=ft.TextStyle(
            shadow = ft.BoxShadow(
                blur_radius = 300,
                # blur_style = ft.ShadowBlurStyle.OUTER,
                color = ft.colors.WHITE
            ),                
        )
        ),
    shadow_color=ft.colors.BLUE,
    elevation=8,
    toolbar_height = 30,
    bgcolor=ft.colors.BLACK38,
    automatically_imply_leading=False,
    ) 

    p = ClassName()
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)
