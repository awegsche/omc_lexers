from pygments.lexer import RegexLexer
from pygments.token import *

class CustomLexer(RegexLexer):
    name = "MadX"
    aliases = ['mad', 'madx']
    filenames = ['*.mad', '*.seq']

    tokens = {
        'root': [
            ('TWISS', Name.Class),
            (r'\btwiss,.*;', Name.Class),
            (r'!.*$', Comment),
            (r'//.*$', Comment),
        ]
    }
