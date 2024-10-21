from selenium_leo1 import SeleniumLeo, By, sleep, getenv, path
from re import findall, sub, search
from DatabaseManager import DatabaseManager


# import pandas as pd
from dotenv import load_dotenv


load_dotenv()
# Acessa a variável de ambiente


class AtualizaTabelaMandados:
    def __init__(self):
        self.navegador_iniciado = False
        self.nometabela = 'tabela.plk'
        self.login_tj = False
        self.selenium = SeleniumLeo(print, modo_oculto=True)
        self.usuario = getenv("USUARIO")
        self.senha = getenv("SENHA")        
        connection_string = getenv("connection_string")
        self.db = DatabaseManager(connection_string, "mandadostjse", pprint=self.pprint)

        self.home = '//*[@id="menuPrincipal"]/ul/li[1]/a/span'
        self.cem = '//*[@id="mov:j_id2"]/option[3]'
        self.campo_login = '//*[@id="loginName"]'
        self.campo_senha = '//*[@id="loginSenha"]'
        self.btn_entrar = '//*[@id="btnEntrar"]/span[2]'
        self.quantidade_de_mandados = '//*[@id="gridAtividades:0:quantidade"]'
        self.proxima_pagina = '//*[@id="mov_paginator_top"]/a[3]'



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
        if path.exists(self.nometabela):
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
   
        self.Escrever_json_db(self.dic_cols_tabela2)


    def Escrever_json_db(self, dic):
        self.db.EditarJson(
            user_id='leomoraes', 
            novos_dados_json=dic,
            tabela = 'mandadostjse'
        ) 


    def pprint(self, *texto):
        print(*texto)


if __name__ == '__main__': 
    at = AtualizaTabelaMandados()
    at.Atualizar_tabela_picle(1)

