# Centralização de estilos e tema customizado
from ttkbootstrap import Style
import config

def apply_theme(style: Style):
    style.theme_create(
        'custom_theme',
        parent='darkly',
        settings={
            'TButton': {
                'configure': {
                    'padding': config.PADDING_DEFAULT,
                    'font': (config.FONT_FAMILY, config.FONT_SIZE_BODY),
                }
            },
            'TRadiobutton': {
                'configure': {
                    'font': (config.FONT_FAMILY, config.FONT_SIZE_BODY),
                }
            },
            'TLabel': {
                'configure': {
                    'font': (config.FONT_FAMILY, config.FONT_SIZE_BODY),
                }
            },
        }
    )
    style.theme_use('custom_theme')
