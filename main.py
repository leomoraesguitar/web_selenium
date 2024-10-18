
import flet as ft
from selenuim_leo import SeleniumLeo, By
from time import sleep






class ClassName(ft.Column):
    def __init__(self):
        super().__init__()

        self.selenium = SeleniumLeo(print)

      
        self.controls = [
            ft.FilledButton(
                text = 'raspar',
                on_click=self.Abrir,
            )
        ]

    def Abrir(self, e):
        link = "https://www.tjse.jus.br/oficialjustica/paginas/movimentacaoMandado/movimentacaoMandado.tjse"

        self.selenium.Abrir_site(link)
        while True:
            sleep(120)          

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
