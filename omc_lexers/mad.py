from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

MAD_CMD_LIST = [
    "twiss",
    "call",
    "use",
    "option",
    "beam",
    "title",
]

MAD_PROP_LIST = [
    "sequence",
    "file",
    "particle",
    "energy",
    "kbunch",
    "npart",
    "bv",
]
class MadLexer(RegexLexer):
    name = "MadX"
    aliases = ['mad', 'madx']
    filenames = ['*.mad', '*.seq']

    tokens = {
        'strings': [
            (r"'.*'", String),
            (r'".*"', String),
        ],
        'root': [
            include('strings'),
            (f'\\b({"|".join(MAD_CMD_LIST)})\\b', Name.Class, 'twiss'),
            (f'\\b({"|".join([x.upper() for x in MAD_CMD_LIST])})\\b', Name.Class, 'twiss'),
            (r'!.*$', Comment),
            (r'//.*$', Comment),
            ("\\bexec", Name.Class, "exec"),
            ("\\b(if|else)", Keyword),
            (r'/\*', Comment.Multiline, 'comment'),
        ],
         'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        'twiss': [
            include('strings'),
            (r';', Text, '#pop'),
            (f'\\b({"|".join(MAD_PROP_LIST)})', Name.Attribute),
            (f'\\b({"|".join([x.upper() for x in MAD_PROP_LIST])})', Name.Attribute),
            (r'[^;]', Text),
        ],
        'exec': [
            ('\\w+', Name.Function),
            ('\\(', Text, "#pop"),
        ]
        
    }
