
from typing import Union
import flet as ft
import os
import pickle
from operator import attrgetter
from re import findall
from datetime import datetime, timedelta



acao1 = ['aguardar', 'cancelar', 'consultar', 'devolver', 'email', 'enviado', 'imp_', 'impresso', 'ligar',
            'Não_encontrei', 'transferido', 'Transferir', 'voltar', 'zap']

tipo1 = ['Afastamento',	'Avaliação',	'Busca',	'Citação',	'Citação e Intimação',	'Condução',	'Contramandado',
            'Entrega',	'Imissão',	'Intimação',	'Intimação para Audiência',' Intimação para Perícia',	'Notificação',	'Ofício',	'Penhora',	'Prisão',	'Reintegração']
tipo1 = list(map(str.upper, tipo1))





class Display(ft.Container):
    def __init__(self,
                 #adicionar clique duplo para abrit campo de txto
            data = None,
            value = None,
            opitions = None, #lista
            height =40,
            width = 120, 
            bgcolor = 'black' ,
            tipos_dados: Union[float, int, str] = [int, float],
            borda_width = 4,
            text_size = 25,
            border_radius = 10,
            func = None,
            on_click = None,
            color = ft.colors.with_opacity(0.7, ft.colors.PRIMARY),
            text_align = 'center', #Optional[TextAlign] = None,
            horizontal_alignment = 'center', #CrossAxisAlignment 
            col = None,
            margin = None,
            border_color = ft.colors.with_opacity(0.2,ft.colors.PRIMARY),         
        ): 
        super().__init__()
        self.opitions = opitions
        self.func = func
        self.on_click = on_click
        self.data = data
        self._color = color
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in opitions]

        self.border_radius =border_radius
        self.borda_width = borda_width
        self.text_size = text_size
        if borda_width > 0:
            self.border = ft.border.all(self.borda_width, border_color)
        else:
            self.border = None
        self.data = data
        self._value = value
        self.bgcolor = bgcolor
        self.height =height
        self.width = width
        self.tipos_dados = tipos_dados
        self.text_align = text_align
        self.horizontal_alignment = horizontal_alignment         
        self._campotexto = ft.TextField(dense=True, on_submit=self.SetarValue)
        self.on_long_press = self.VirarCampoTexto
        self.col = col
        self.margin = margin
        self.GerarContent()

    def GerarContent(self):
        self.content = ft.PopupMenuButton(
            content=ft.Column(
                [
                    ft.Text(
                        self._value, 
                        color=self._color,
                        weight='BOLD', 
                        size=self.text_size, 
                        no_wrap = False,
                        text_align = 'center' 
                    )
                ], 
                alignment='center', 
                horizontal_alignment='center'
            ),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER
        )        

    def SetarValue(self,e):
        self._value = self._campotexto.value
        self.GerarContent()
        if not self.func is None:
            self.func(self._value)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()     

    def VirarCampoTexto(self,e):
        content_antigo = self.content
        self.content = self._campotexto
        if not self.on_click is None:
            self.on_click(e)  
        self.Atualizar()
     
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, cor):
        self._color = cor  
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }        

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,        
        )
         
        self.Atualizar()




    def Clicou(self,e):
        if type(e.control.text) in [int, float]:
            valor = round(e.control.text,1)
        else:
           valor = e.control.text 
        self.content.content.controls[0].value = valor
        self._value = valor

        if not self.func is None:
            self.func(valor)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()



    @property
    def value(self):
        try:
            v = int(self._value)
        except:
            try:
                v = float(self._value)
            except:            
                v = self._value
        return v



    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    @value.setter
    def value(self, valor):
        if isinstance(self.content, ft.PopupMenuButton):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.items.append(ft.PopupMenuItem(valor, on_click = self.Clicou))
                self.content.content.controls[0].value = valor
                self.Atualizar()
            else:
                print('número inválido')
        elif isinstance(self.content, ft.TextField):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.value = valor
                self.Atualizar()
            else:
                print('número inválido')
 


class CampoTexto(ft.Row):
    def __init__(self, texto, width, isdestinaraio = False, color = None, index = None, func = None,):
        super().__init__() 
        self.spacing=0
        self.run_spacing = 0
        self.index = index
        self.func = func
        self.texto = texto
        self._color = color
        self.alignment = ft.MainAxisAlignment.CENTER
        # self.tight = True
        # self.wrap = True
        self.width = width
        if self._color:
            pass
        else:
            self._color = ft.colors.PRIMARY if isdestinaraio else  ft.colors.with_opacity(0.7, ft.colors.PRIMARY)
        

        if not self.index is None: 
            if self.index[1] in ['Destinatario do mandado:']:
                self.controls = [
                    ft.IconButton(
                        icon = ft.icons.SEARCH, 
                        scale = 1, 
                        height=25,
                        icon_size = 10, 
                        alignment = ft.alignment.center,
                        width=18, 
                        data = [self.index[0],'pesquisar',1], 
                        on_click=self.func, 
                        tooltip = 'Pesquisar contato no zap'
                    ),
                    ft.Text(
                        texto,                 
                        text_align='center',
                        selectable = True,
                        color = self._color,
                        weight  = ft.FontWeight.W_900 if isdestinaraio else None,
                        width = width-30,
                    ),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        splash_radius = 0,
                        height=25,
                        icon_size = 10 , 
                        width=12,    
                        data = texto,            
                        alignment = ft.alignment.center,
                        padding = ft.Padding(0,0,0,0),
                        style = ft.ButtonStyle(
                            padding =ft.Padding(0,0,0,0),
                        ),
                        on_click=self.Copiar
                    )

                ]            
            

            elif self.index[1] in ['Nº do mandado:']:
                self.controls = [
                    ft.IconButton(
                        icon = ft.icons.PICTURE_AS_PDF, 
                        scale = 1, 
                        height=25,
                        icon_size = 10, 
                        width=18, 
                        alignment = ft.alignment.center,
                        data = [self.index[0],'ver_pdf',1], 
                        on_click=self.func, 
                        tooltip = 'Visualizar PDF'
                    ),
                    ft.Text(
                        texto,                 
                        text_align='center',
                        selectable = True,
                        color = self._color,
                        weight  = ft.FontWeight.W_900 if isdestinaraio else None,
                        width = width-30,
                    ),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        splash_radius = 0,
                        height=25,
                        icon_size = 10 , 
                        width=12,    
                        data = texto,            
                        alignment = ft.alignment.center,
                        padding = ft.Padding(0,0,0,0),
                        style = ft.ButtonStyle(
                            padding =ft.Padding(0,0,0,0),
                        ),
                        on_click=self.Copiar
                    )

                ]



        else:
            # print('02')
            self.controls = [
                ft.Text(
                    texto,                 
                    text_align='center',
                    selectable = True,
                    color = self._color,
                    weight  = ft.FontWeight.W_900 if isdestinaraio else None,
                    width = width-12,
                ),
                ft.IconButton(
                    icon=ft.icons.COPY,
                    splash_radius = 0,
                    height=25,
                    icon_size = 10 , 
                    width=12,    
                    data = texto,            
                    alignment = ft.alignment.center,
                    padding = ft.Padding(0,0,0,0),
                    style = ft.ButtonStyle(
                        padding =ft.Padding(0,0,0,0),
                    ),
                    on_click=self.Copiar
                )

            ]

    def Copiar(self, e):
        e.page.set_clipboard(e.control.data)
        # self.pprint(f"({e.control.data}) copiado para a área de transferência")

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        if not self.index is None:
            self.controls[0].icon_color = self._color
            self.controls[1].color = self._color
            self.controls[2].icon_color = self._color

        else:
            self.controls[0].color = self._color
            self.controls[1].icon_color = self._color
        try:
            self.update()
        except:
            pass

    @property
    def value(self):
        return self.texto
    
    @value.setter
    def value(self, value):
        pass


class FinalDePraxo(ft.TextField):
    def __init__(self, valor, larguras, nome):
        super().__init__()
        self.value = valor 
        self.width = larguras.get(nome, 80)
        self.text_align='center'
        self.selectable=True
        self.color=ft.colors.with_opacity(0.8, ft.colors.PRIMARY)

             


class Linha(ft.Container):
    def __init__(self, larguras, valores, bgcolor = None, nomes_colunas = None, index = None, funcao = None ):
        super().__init__()
        self.bgcolor = bgcolor
        self.index = index
        self.padding=ft.padding.symmetric(18,0)
        self.margin = ft.margin.symmetric(0,0)
        self.funcao = funcao
        self.nomes_colunas = nomes_colunas
        self.valores = valores
        '''
        self._processo = CampoTexto(
            valores[0],
            larguras['Nº do Processo:']
        )
        self._mandado = CampoTexto(
            valores[1], 
            larguras['Nº do mandado:'],
            
        )
        self._Destinatario = CampoTexto(
            valores[2], 
            larguras['Destinatario do mandado:'], 
            isdestinaraio=True,                      
        )      
        self._Endereco = ft.Text(
            valores[3], 
            width = larguras['Endereco'],
            size = 10,
            text_align='center',
            selectable=True,
        )
        self._Situação = ft.Text(
            valores[4], 
            width = larguras['Situação'],
            text_align='center',
            selectable=True,
        )
        self._Prioridade = ft.Text(
            valores[5], 
            width = larguras['Prioridade'],
            text_align='center',
            selectable=True,
        )
        self._Audiência = ft.Text(
            valores[6], 
            width = larguras['Audiência'],
            text_align='center',
            selectable=True,
        )
        self._Recebimento = ft.Text(
            valores[7], 
            width = larguras['Recebimento'],
            text_align='center',
            selectable=True,
        )
        self._prazo = ft.Text(
            valores[8], 
            width = larguras['Final de prazo'],
            text_align='center',
            selectable=True,
        )
        self._acao = Display(
            value = valores[9], 
            opitions = acao1,
            width = larguras['ação'],
            text_align='center',
            borda_width = 0,
            text_size = 15,
            bgcolor=ft.colors.TRANSPARENT,
            # data=[indx[l],'acao2',[l,num_col], k],
            data='acao2',
            on_click=self.Func3
        )    
        self._Tipo = Display(
            value = valores[10], 
            opitions = tipo1,
            width = larguras['Tipo do mandado:'],
            text_align='center',
            borda_width = 0,
            text_size = 15,
            bgcolor=ft.colors.TRANSPARENT,
            # data=[indx[l],'tipo2',[l,num_col], k],
            data='tipo2',
            on_click=self.Func3            

        )
        self._telefone = CampoTexto(
            valores[11], 
            larguras['telefone'],
 
        ) 
        '''
        self.objetos = {}
        for i in nomes_colunas:
            if i == 'Tipo do mandado:':
                self.objetos[i] = Display(
                    value = valores[self.nomes_colunas.index(i)], 
                    opitions = tipo1,
                    width = larguras.get(i, 80),
                    text_align='center',
                    borda_width = 0,
                    text_size = 15,
                    bgcolor=ft.colors.TRANSPARENT,
                    data=[self.index,'tipo2',1, 1, i],
                    # data='tipo2',
                    on_click=self.Func3            
                )
            elif i == 'ação':
                valor = valores[self.nomes_colunas.index(i)]
                self.objetos[i] = Display(
                    value = valor,
                    opitions = acao1,
                    width = larguras.get(i, 80),
                    text_align='center',
                    borda_width = 0,
                    text_size = 15,
                    bgcolor=ft.colors.TRANSPARENT,
                    data=[self.index,'acao2',1, 1, i],
                    # data='acao2',
                    on_click=self.Func3
                ) 
                self.bgcolor = self.Cores(valor)  
            elif i in ['Nº do Processo:','telefone' ]:
                self.objetos[i] = CampoTexto(
                    valores[self.nomes_colunas.index(i)], 
                    larguras.get(i, 120),
                ) 
            elif i in ['Nº do mandado:' ]:
                # print(f'self.index = {self.index}')
                self.objetos[i] = CampoTexto(
                    valores[self.nomes_colunas.index(i)], 
                    larguras.get(i, 120),
                    index = [self.index,'Nº do mandado:'],
                    func=self.Func
                )               

            elif i in ['Destinatario do mandado:']:
                self.objetos[i] = CampoTexto(
                    valores[self.nomes_colunas.index(i)], 
                    larguras.get(i, 80),
                    isdestinaraio=True, 
                    index = [self.index,'Destinatario do mandado:'],
                    func=self.Func,

                ) 
            elif i in ['Endereco']:
                self.objetos[i] = ft.Text(
                    value = valores[self.nomes_colunas.index(i)], 
                    width = larguras.get(i, 80),
                    text_align='center',
                    selectable=True,
                    size = 10,
                    color=ft.colors.with_opacity(0.8, ft.colors.PRIMARY),
                )


            elif i in ['Final de prazo', 'Recebimento', 'Audiência']:
                valor = valores[self.nomes_colunas.index(i)]
                self.objetos[i] = ft.Text(
                    value = valor, 
                    width = larguras.get(i, 80),
                    text_align='center',
                    selectable=True,
                    data = self.excel_date_converter(valor),
                    color=ft.colors.with_opacity(0.8, ft.colors.PRIMARY),

                )

                                             
            else:
                # print(self.nomes_colunas)
                # print(self.nomes_colunas.index(i))
                self.objetos[i] = ft.Text(
                    value = valores[self.nomes_colunas.index(i)], 
                    width = larguras.get(i, 80),
                    text_align='center',
                    selectable=True,
                    color=ft.colors.with_opacity(0.8, ft.colors.PRIMARY),

                )

         


        if 'Final de prazo' in self.nomes_colunas:
                def converter_para_datetime(data_string):
                    return datetime.strptime(data_string, "%d/%m/%Y %H:%M:%S")
                def next_thursday():
                    today = datetime.now().date()
                    # Calcula quantos dias faltam para a próxima quinta-feira
                    days_until_thursday = (3 - today.weekday()) % 7
                    if days_until_thursday == 0:
                        # Caso hoje seja quinta-feira, pegamos a próxima
                        days_until_thursday = 7
                    # Retorna a data da próxima quinta-feira
                    return today + timedelta(days=days_until_thursday)

                def compare_date_with_next_thursday(date_str):
                    # Converte a data fornecida para o número Excel
                    given_date_excel = self.excel_date_converter(date_str)
                    
                    # Converte a próxima quinta-feira para o número Excel
                    next_thursday_date = next_thursday()
                    next_thursday_excel = self.excel_date_converter(next_thursday_date.strftime("%d/%m/%Y 00:00:00"))
                    
                    # Retorna True se a data fornecida for menor que a próxima quinta-feira
                    return given_date_excel < next_thursday_excel  
                        
                # prazo = findall(r'(\d{2}/\d{2}/\d{4})', self.objetos.get('Final de prazo',None).value)[0]
                prazo = self.objetos.get('Final de prazo',None).data

                cor2  = 'primary,0.7'
                # print('prazo:', prazo)
                # Função para converter string "dd/mm/yy" para datetime
                # print('len(prazo):',len(prazo))
            
                next_thursday_date = next_thursday()
                next_thursday_excel = self.excel_date_converter(next_thursday_date.strftime("%d/%m/%Y 00:00:00"))
                
                # Retorna True se a data fornecida for menor que a próxima quinta-feira
                # return given_date_excel < next_thursday_excel                     
                if prazo < next_thursday_excel:
                    # cor2  = 'red,0.5'
                    self.bgcolor = '#670707'

                    
                elif prazo < next_thursday_excel + 8:
                    cor2  = '#110000'
                    self.bgcolor = '#b1cc18'
                    for i in self.objetos.items():
                        i[1].color = cor2
                        # i[1].update()
                        # print(i[1].color)
                    
                    
               


        self.content = ft.Row(
            vertical_alignment = ft.CrossAxisAlignment.START,
            controls = [
                i for n,i in self.objetos.items()
            ]               

        )


        # x = 35
        # self.content.controls.append(
        #     ft.Row(
        #         [
        #             ft.IconButton(icon=ft.icons.SEND, width=x,alignment = ft.alignment.center,icon_color = cor2,
        #             tooltip=f"Enviar Mandado \npara {self.objetos.get('Destinatario do mandado:', 'nome')}", on_click=self.Func,
        #             data=[self.index,'enviar']),

        #             ft.IconButton(icon=ft.icons.PICTURE_AS_PDF_OUTLINED,width=x,alignment = ft.alignment.center,
        #                 tooltip='Enviar PDF para o \ncontato aberto no zap', icon_color = cor2,
        #                 on_click=self.Func, data=[self.index,'pdf',1]),
                        
        #             ft.IconButton(icon=ft.icons.PERM_CONTACT_CAL_ROUNDED,width=x,alignment = ft.alignment.center,
        #                     tooltip='Add Contato', icon_color = cor2,
        #                     on_click=self.Func, data=[self.index,'add']),  

        #             ft.IconButton(icon=ft.icons.CANCEL_SCHEDULE_SEND_OUTLINED,alignment = ft.alignment.center,
        #                 width=x, tooltip='Enviar Mandado direto \npara o contato \naberto no zap', icon_color = cor2,
        #                 on_click=self.Func, data=[self.index,'Mand.D',1]), 
                       
        #             ft.Text(width=20)           
        #         ], 
        #         spacing=0
        #     )
        # )
             

    def excel_date_converter(self, date_str):
        # Converte a string em formato de data e hora para um objeto de data (ignora o tempo)
        date_format = "%d/%m/%Y %H:%M:%S"
        
        # Parse da string para objeto datetime
        if len(date_str) < 6:
            date_str = "30/12/2080 07:00:00"
        try:
            dt = datetime.strptime(date_str, date_format)
        except:
            date_format = "%d/%m/%Y %H:%M"
            dt = datetime.strptime(date_str, date_format)


        
        # Converte a data para um número Excel (dias a partir de 01/01/1900)
        base_date = datetime(1899, 12, 30)  # Data de referência usada pelo Excel
        
        # Subtrai as datas para obter a diferença em dias e retorna como número inteiro
        return (dt.date() - base_date.date()).days



    def Func(self, e):
        encontrou = False

        if e.control.data[1] in ['Mand.D','pdf']:
            if 'ação' in self.nomes_colunas:
                self.valores[self.nomes_colunas.index('ação')] = 'enviado'                
                self.objetos.get('ação', None).value = 'enviado'
                self.bgcolor = self.Cores('enviado')
                self.Atualizar()
        # pass
        if self.funcao:
            self.funcao(e)

    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    def Cores(self, texto):
        match texto:
            case 'zap':
                cor = '#1a2a18' 
            case 'ligar':
                cor = '#636363'                 
            case 'enviado':
                cor = '#3e163a'                          
            case 'aguardar':
                cor = '#072e5b'                        
            case 'impresso':
                cor = '#202933'     
            case 'devolver':
                cor = '#5e5858'
            case 'imp_':
                cor = '#0a0c2f'
            case 'Transferir':
                cor = '#353f42'                                                                                                                  
            case _:
                cor = 'black' 
        return cor


                                                                                                                   
    def Func3(self,e):
        cor = self.Cores(e.control.text)    
        cor_old = self.bgcolor
          
        if e.control.data[1] == 'acao2' and cor_old not in [ft.colors.YELLOW_500, ft.colors.RED_900]:
            self.bgcolor = cor
        self.valores[self.nomes_colunas.index(e.control.data[4])] = e.control.text
        # self._df.iloc[e.control.data[2][0],e.control.data[2][1]] = e.control.text
        try:
            self.update()
        except:
            pass
        if self.funcao:
            self.funcao(e)

    '''
    @property
    def processo(self):
        return self._processo.value

    @processo.setter
    def processo(self, valor):
        self._processo.value = valor


    @property
    def mandado(self):
        return self._mandado.value

    @mandado.setter
    def mandado(self, valor):
        self._mandado.value = valor


    @property
    def Destinatario(self):
        return self._Destinatario.value

    @Destinatario.setter
    def Destinatario(self, valor):
        self._Destinatario.value = valor


    @property
    def Endereco(self):
        return self._Endereco.value

    @Endereco.setter
    def Endereco(self, valor):
        self._Endereco.value = valor


    @property
    def Situação(self):
        return self._Situação.value

    @Situação.setter
    def Situação(self, valor):
        self._Situação.value = valor


    @property
    def Prioridade(self):
        return self._Prioridade.value

    @Prioridade.setter
    def Prioridade(self, valor):
        self._Prioridade.value = valor


    @property
    def Audiência(self):
        return self._Audiência.value

    @Audiência.setter
    def Audiência(self, valor):
        self._Audiência.value = valor


    @property
    def Recebimento(self):
        return self._Recebimento.value

    @Recebimento.setter
    def Recebimento(self, valor):
        self._Recebimento.value = valor


    @property
    def prazo(self):
        return self._prazo.value

    @prazo.setter
    def prazo(self, valor):
        self._prazo.value = valor


    @property
    def acao(self):
        return self._acao.value

    @acao.setter
    def acao(self, valor):
        self._acao.value = valor


    @property
    def Tipo(self):
        return self._Tipo.value

    @Tipo.setter
    def Tipo(self, valor):
        self._Tipo.value = valor


    @property
    def telefone(self):
        return self._telefone.value

    @telefone.setter
    def telefone(self, valor):
        self._telefone.value = valor
    '''






class Classificador(ft.Container):
    def __init__(self,
                 value = 'valor',
                 func = None,
                 width = None,
                height = None,
                theme_style = ft.TextThemeStyle.TITLE_MEDIUM,
                color = None,
                data = None
                 ):
        super().__init__()
        # self.tight=True
        # self.spacing=0
        # self.height=200
        # self.run_spacing=0  
        # self.width =  width
        self.height = height
        self.theme_style = theme_style
        self.color = color
        self.value = value    
        self.func = func
        self.data = data
        self.seta = True
        self.icone = ft.Icon(ft.icons.ARROW_UPWARD, visible=False, size = 13)
        self.alignment = ft.alignment.top_center
        self.padding = 0
        self.margin = 0
        self.texto =  ft.Text(
                    self.value,
                    # spans = [ft.TextSpan(self.value),ft.TextSpan(style = ft.TextStyle(weight = 'BOLD', size = 20))], 
                    theme_style=self.theme_style,
                    color = self.color,
                    width = width-10,
                    text_align = 'center',
                    weight=ft.FontWeight.W_900,
                    size = 12 if self.value in ['Audiência', ] else None,
                )
                    
        self.texto2 = ft.Text(
            data = True, 
            color = ft.colors.CYAN,
            style = ft.TextStyle(
                weight = 'BOLD', 
                size = 20
            )
        )
        self.content = ft.Row(
            [
            self.texto,self.texto2
                # self.icone
            ], 
            width=width if not width is None else None, 
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment = ft.MainAxisAlignment.CENTER,
            spacing=0,
            run_spacing=0,
        )
        self.on_click=self.Clicou
   

    def Clicou(self, e):
        self.seta = not self.seta
        # self.icone.visible = True
        # if self.seta:
        #     self.icone.name = ft.icons.ARROW_DOWNWARD
        # else:
        #     self.icone.name = ft.icons.ARROW_UPWARD

        self.texto2.data = not self.texto2.data
        if self.seta:
            self.texto2.value = "↑"
        else:
            self.texto2.value = "↓"

        if not self.func is None:
            self.func(e)
        try:
            self.update()
        except:
            pass


class ResponsiveTablle(ft.Row):
    def __init__(self, tabela, funcao = None):
        super().__init__()
        self.scroll = ft.ScrollMode.HIDDEN
        self.funcao = funcao
        self.expand = True
        self.larguras = {
            'Nº do Processo:':120, 
            'Nº do mandado:':135, 
            'Destinatario do mandado:':220,
            'Endereco':200, 
            'Situação': 80,
            'Recebimento':110,
            'Prioridade':90,
            'ação':80, 
            'Tipo do mandado:':92, 
            'Audiência':70,
            'Final de prazo':100, 
            'telefone':120,
            'Funções':160
        }
        self.tabela = self.remover_zap(tabela)
        self.TIPO = True if not isinstance(self.tabela, dict) else False
        self.nomes_colunas = list(self.tabela.columns) if self.TIPO else list(self.tabela.keys())
        self.num_linhas = self.tabela.shape[0] if self.TIPO else len(self.tabela[list(self.tabela.keys())[0]])
        label_style = ft.TextStyle(
            size = 12,
            
        )
        self.objetos_colunas = {i:ft.Checkbox(i, data = i, label_style = label_style, value = False, on_change=None) for i in self.nomes_colunas}
        self.ver_colunas = ft.Container(
                bgcolor = 'grey800,0.9',
                border_radius=12,
                padding=ft.Padding(10,0,10,0),                
                alignment=ft.alignment.center,
                content = ft.Row(
                    vertical_alignment='center',
                    alignment='center',
                    # tight=True,
                    expand_loose=True,
                    controls = [
                        self.objetos_colunas.get(i, None)
                        for i in self.nomes_colunas 
                    ]
                ), 
        ) 
            
        self.pesquisar_na_tabela = ft.TextField(
                hint_text = 'Pesquisar',
                tooltip = 'Pesquisar palavra na tabela',
                border_width=1,
                # dense=True,
                text_size = 15,
                on_change=self.Pesquisar1,
                
                # cursor_height = 12,
                prefix=ft.Container(
                    ft.Icon(
                        name = ft.icons.SEARCH,
                        size = 15,
                    ),
                    alignment=ft.alignment.center_left,
                    padding=0,
                    width=15,
                ),

                border_radius=40,
                filled=True,
                
                height=30,
                # width=130,
                autofocus = True,
                col = 2,
                content_padding=ft.Padding(5,5,0,0)
            ) 

        self.exibirNum_mandados = ft.Text(f'{self.num_linhas} mandados', color = 'primary', col = 1)

        self.linha_atalhos = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=40,
            run_spacing=0,
            tight=True,
            height=25,
            # columns = 12,
            # width=900,
            # expand_loose=True,
            controls = [
                ft.Checkbox(
                    splash_radius=0,
                    # scale=0.6,
                    label = i,
                    label_style = ft.TextStyle(
                        color = ft.colors.PRIMARY,
                    ),
                    shape=ft.CircleBorder(),
                    on_change=self.Pesquisarchek,
                    col = 1,
                )
                for i in ['zap', 'imp_', 'impresso', 'devolver', 'enviado']

            ]+[self.pesquisar_na_tabela,self.exibirNum_mandados]
        ) 
        a = sum([i.col for i in self.linha_atalhos.controls])
      
        # self.linha_atalhos.columns = a

        self.header =  ft.Container(
                bgcolor = 'grey900,0.99',
                padding=ft.padding.symmetric(12,0),
                border=ft.border.all(0.5, ft.colors.PRIMARY),
                border_radius=ft.BorderRadius(
                    20,20,0,0
                ),
                content = ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    run_spacing=0,
                    # width=600,
                    expand=True,
                    controls = [
                        self.linha_atalhos,  
                        ft.Text('_'*120, text_align='center', color = 'primary', expand_loose=True, overflow=ft.TextOverflow.CLIP ),                 
                        ft.Row(
                            vertical_alignment='center',
                            tight=True,
                            wrap=True,
                            controls = [
                                Classificador(
                                    value = i,
                                    width = self.larguras.get(i, 80),
                                    data = i,
                                    color = 'primary',
                                    func=self.Ordenar_por

                                )
                                for i in self.nomes_colunas #+ ['Funções']
                            ]
                        ), 

                    ]
                )
                


                    
        ) 
        


        self.boddy =  ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
            spacing=0.9,
            run_spacing=0,
            
        )
        self.CarregarLinhas()

        self.controls = [
            ft.Column(
                # scroll=ft.ScrollMode.HIDDEN,
                # expand=True,
                
                controls = [
                    self.header,
                    ft.Container(
                        border_radius=ft.BorderRadius(
                            0,0,20,20
                        ),
                        border=ft.border.all(0.5, ft.colors.PRIMARY),
                        content = self.boddy,
                        expand=True,
                    ),
                    
                    # self.ver_colunas,
                   
                ],
                spacing=0,
                run_spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),            
        ]
        
      

    def CarregarLinhas(self):
        self.df_lista = self.tabela.values.tolist() if self.TIPO else self.dicionario_para_lista_de_listas(self.tabela)
        self.indx = list(self.tabela.index) if self.TIPO else [i for i in range(self.num_linhas)]
        for n, linha in zip(self.indx,self.df_lista):
            bgcolor =  'black' if n%2 == 0 else 'grey900,0.99'
            # print(f'n = {n}')
            self.boddy.controls.append(
                Linha(self.larguras,linha,bgcolor,self.nomes_colunas,n, self.Change)
            )



    def OrdenarListadeClasses(self, lista, data, decrecente=True):
        # return sorted(lista, key=attrgetter(atributo), reverse=decrecente) 
        if data in ['Final de prazo', 'Recebimento', 'Audiência']:
            return sorted(lista, key=lambda x: x.objetos[data].data, reverse=decrecente)    
        else:
            return sorted(lista, key=lambda x: x.objetos[data].value, reverse=decrecente)    


    def dicionario_para_lista_de_listas(self, dicionario):
        """
        Converte um dicionário em uma lista de listas.
        
        Args:
        dicionario (dict): O dicionário a ser convertido.
        
        Returns:
        list: Lista de listas onde cada sublista contém os valores correspondentes a cada chave do dicionário.
        """
        # Obter todas as chaves do dicionário
        chaves = list(dicionario.keys())
        
        # Inicializar a lista de listas
        lista_de_listas = []
        
        # Obter o número de elementos em cada lista do dicionário
        num_elementos = len(dicionario[chaves[0]])
        
        # Preencher a lista de listas com os valores do dicionário
        for i in range(num_elementos):
            sublista = [dicionario[chave][i] for chave in chaves]
            lista_de_listas.append(sublista)
        
        return lista_de_listas



    def Ordenar_por(self, e):
        data = e.control.data
        # data2  =  {'Nº do Processo:':'processo', 
        #     'Nº do mandado:':'mandado', 
        #     'Destinatario do mandado:':'Destinatario',
        #     'Endereco':'Endereco', 
        #     'Situação': 'Situação',
        #     'Recebimento':'Recebimento',
        #     'Prioridade':'Prioridade',
        #     'ação':'acao', 
        #     'Tipo do mandado:':'Tipo', 
        #     'Audiência':'Audiência',
        #     'Final de prazo':'prazo', 
        #     'telefone':'telefone'
        # }
        # atr = data2[data]
        lista = [i for i in self.boddy.controls]

        lista = self.OrdenarListadeClasses(lista, data, decrecente = e.control.seta)
        self.boddy.controls = []
        for n, k in enumerate(lista):
            # k.bgcolor =  'black' if n%2 == 0 else 'grey900,0.99'
            self.boddy.controls.append(k)
        self.boddy.update()     
        
    def Change(self, e):
        # print(e.control.text)
        if self.funcao:
            self.funcao(e)


    def remover_zap(self, df):
        if not isinstance(df, dict):
            if 'zap' in df.columns:
                df = df.drop(columns=['zap'])
            return df
        elif 'zap' in list(df.keys()):
            del df['zap']
        return df

            
            





    def Pesquisar1(self, e):
        palavra = e.control.value
        def LimparPesquisa(e):
            self.pesquisar_na_tabela.suffix=None
            self.pesquisar_na_tabela.value = ''
            self.Pesquisar('')
            self.exibirNum_mandados.value = f'{self.num_linhas} mandados'
            self.exibirNum_mandados.update()            
            self.update()
            self.pesquisar_na_tabela.update()   

        if palavra not in ['', None]:
            if e.control.suffix == None:          
                e.control.suffix=ft.Container(
                    ft.Icon(
                        name = ft.icons.CANCEL,
                        size = 15,
                        color = 'primary, 0.8',
                    ),
                    alignment=ft.alignment.center_left,
                    padding=ft.Padding(0,0,0,0),
                    margin=ft.Margin(0,0,5,8),
                    width=20,
                    height=15,
                    on_click=LimparPesquisa,
                    # bgcolor='red'
                )  
                e.control.update()            
            self.Pesquisar(palavra)
            self.exibirNum_mandados.value = f'{self.num_linhas} mandados'
            self.exibirNum_mandados.update()
            self.update()
        else:
            pass
    def Pesquisar2(self, palavra):
        # self.pesquisa_em_curso = True

        # def LimparPesquisa(e):
        #     # self.pesquisar.suffix=None
        #     # self.pesquisar.value = ''
        #     l = []
        #     for i, j in self.arq_abrev.items():
        #         # if palavra in i or palavra in j or palavra.capitalize() in i or palavra.capitalize() in j:
        #         l.append(Aabrev(i, j) )
        #     # l = [Aabrev(i, j) ]
        #     l = self.OrdenarListadeClasses(l)
        #     self.controls[0].controls = l  
        #     self.controls[0].update()            
        #     self.pesquisar.update()

        # if e.control.suffix == None:          
        #     e.control.suffix=ft.Container(
        #         ft.Icon(
        #             name = ft.icons.CANCEL,
        #             size = 15,
        #             color = 'primary, 0.8',
        #         ),
        #         alignment=ft.alignment.center_left,
        #         padding=ft.Padding(0,0,0,0),
        #         margin=ft.Margin(0,0,5,5),
        #         width=20,
        #         height=15,
        #         on_click=LimparPesquisa,
        #         # bgcolor='red'
        #     )  
        #     e.control.update()

        # palavra = e.control.value
        if palavra in ['', None]:
            self.boddy.controls = []
            for n, linha in zip(self.indx,self.df_lista):
                bgcolor =  'black' if n%2 == 0 else 'grey900,0.99'.upper()
                self.boddy.controls.append(
                    Linha(self.larguras,linha,bgcolor,self.nomes_colunas,n, self.Change)
                )
            self.num_linhas = self.tabela.shape[0]                
                           
        else:
            self.boddy.controls = []
            for n, linha in zip(self.indx,self.df_lista):
                bgcolor =  'black' if n%2 == 0 else 'grey900,0.99'.upper()
                for p in linha:
                    if palavra in p  or palavra.capitalize() in p or palavra.upper() in p:
                        self.boddy.controls.append(
                            Linha(self.larguras,linha,bgcolor,self.nomes_colunas,n, self.Change)
                        )
                        break
            self.num_linhas = len(self.boddy.controls)
        # self.boddy.update()
        # self.update()


    def Pesquisar(self, palavra):
        self.num_linhas = 0
        if palavra in ['', None]:              
            for i in self.boddy.controls:
                    i.visible =True
                    self.num_linhas +=1                                      
        else:
            for linha in self.boddy.controls:
                linha.visible =False
                for p in linha.valores:
                    if palavra in p  or palavra.capitalize() in p or palavra.upper() in p:
                        linha.visible =True
                        self.num_linhas +=1
                        break                        

        self.boddy.update()
        self.update()






    def Pesquisarchek(self, e):
        if e.control.value == True:
            for i in self.linha_atalhos.controls:
                if isinstance(i, ft.Checkbox) and i!= e.control:
                    i.value = False
            palavra = e.control.label
            self.Pesquisar(palavra)
            self.exibirNum_mandados.value = f'{self.num_linhas} mandados'
            self.exibirNum_mandados.update()             
        else:
            self.Pesquisar('')
            self.exibirNum_mandados.value = f'{self.num_linhas} mandados'
            self.exibirNum_mandados.update()             

        self.update()



def main(page: ft.Page):
    larg = 1295
    page.window.width = larg
    class Verificar_pasta:
        def __init__(self,pastalocal = 'tabelamandadostjse'):
            self.pastalocal = pastalocal
            self.verificar_pasta()

        def verificar_pasta(self):
            user_profile = os.environ.get('USERPROFILE')
            # print(user_profile)
            if not user_profile:
                # return False  # USERPROFILE não está definido
                self.local = None

            caminho = os.path.join(user_profile, self.pastalocal)
            
            if os.path.exists(caminho):
                self.local = caminho
                # return self.caminho
            else:
                os.mkdir(caminho)
                # print(caminho)
                if os.path.exists(caminho):
                    self.local = caminho
                    # return self.caminho
                # else:
                    # return None
        

        def caminho(self, nome):
            # self.verificar_pasta()
            return os.path.join(self.local, nome)


    # nometabela = Verificar_pasta('tabelamandadostjse').caminho('tabela.plk')
    nometabela = r'assets\tabelajoson.plk'


    def LerPickle(nome):
        if not nome.endswith('.plk'):
            nome += '.plk'
        if os.path.isfile(nome):
            with open(nome, 'rb') as arquivo:
                return pickle.load(arquivo)
        else:
            return None    



    tabela = LerPickle(nometabela)

    p = ResponsiveTablle(tabela)    #.iloc[:,2:6]
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)
