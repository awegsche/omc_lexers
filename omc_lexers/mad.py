from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

# for general cmds (we don't care if the attributes are correct)
# this should be absorbed over time to a more detailled approach
MAD_CMD_LIST = [
    "TWISS",
    "TITLE",
    "VALUE",
    "HELP",
    "SHOW"
]

MAD_PROP_LIST = [
    "SEQUENCE",
    "FILE",
    "PARTICLE",
    "ENERGY",
    "KBUNCH",
    "NPART",
    "BV",
]

MAD_OPTIONS = [
    "INFO",
    "ECHO(MACRO)?",
    "VERBOSE",
    "WARN",
    "TRACE",
    "VERIFY",
    "TELL",
    "RESET",
    "NO_FATAL_STOP",
    "KEEP_EXP_MOVE",
    "RBARC",
    "THIN_FOC",
    "BBORBIT",
    "SYMPL",
    "TWISS_PRINT",
    "THREADER"
]

MADX_BUILTIN_FN = [
    "SQRT",
    "LOG",
    "LOG10",
    "EXP",
    "SIN",
    "COS",
    "TAN",
    "ASIN",
    "ACOS",
    "ATAN",
    "SINH",
    "COSH",
    "TANH",
    "SINC",
    "ABS",
    "ERF",
    "ERFC",
    "FLOOR",
    "CEIL",
    "ROUND",
    "FRAC",
    "RANF",
    "T?GAUSS"
]

MAD_KEYWORD = [
    "IF",
    "ELSE",
    "ELSEIF",
    "WHILE",
    "TRUE",
    "FALSE",
]

def add_command(name, aliases=None, token=Name.Class, no_scope=False):
    if aliases is None:
        aliases = [name]
    if no_scope:
        return (f'(?i)\\b({"|".join(aliases)})\\b', token)
    else :
        return (f'(?i)\\b({"|".join(aliases)})\\b', token, name)

def make_command(attrs):
    return [
        include('strings'),
        (r';', Text, '#pop'),
        (f'(?i)\\b({"|".join(attrs)})(\\s*=\\s*\\w+)?', bygroups(Name.Attribute, Text)),
        include('punct'),
        ('.', Text),
        #(r'[^;]', Text),
    ]

class MadLexer(RegexLexer):
    name = "MadX"
    aliases = ['mad', 'madx']
    filenames = ['*.mad', '*.madx', '*.seq']

    tokens = {
        'strings': [
            (r"'.*?'", String),
            (r'".*?"', String),
        ],
        'punct': [
            # skip any unknown identifier
            ("[\\w+\\.]", Text),
            # punctuation and operators
            ("[,;\\(\\)]\\s*", Text),
            ("\\s*[\\+\\-\\*\\/]\\s*", Text),
            ("\\s*:?=\\s*", Operator),
            ("=", Operator),
        ],
        'root_cmds': [
            # general fall back highlighting, will vanish over time
            (f'(?i)\\b({"|".join(MAD_CMD_LIST)})\\b', Name.Class, 'twiss'),
            (f'(?i)\\b({"|".join(MADX_BUILTIN_FN)})\\b', Name.Class),
            # the MADX commands
            add_command('option'),
            add_command('set'),
            add_command('select'),
            add_command('use'),
            add_command('system', ['system', 'title'], no_scope=True),
            add_command('assign'),
            add_command('call', aliases=["CALL", "REMOVEFILE"]),
            add_command('print'),
            add_command('printf'),
            add_command('renamefile'),
            add_command('chdir'),
            add_command('copyfile'),
            add_command('create'),
            add_command('delete'),
            add_command('readmytable', aliases=["READMYTABLE", "WRITE", "READTABLE"]),
            add_command('fill', aliases=["FILL", "SHRINK"]),
            add_command('setvars'),
            add_command('fill_knob'),
            add_command('setvars_lin'),
            add_command('beam'),
            add_command('resbeam'),
            ("SEQEDIT", Name.Class, 'seqedit'),
            # comments
            (r'!.*$', Comment),
            (r'//.*$', Comment),
            (r'/\*', Comment.Multiline, 'comment'),
            # the exec command
            ("(?i)\\bexec", Name.Class, "exec"),
            # keywords
            add_command("kw", aliases=MAD_KEYWORD, token=Keyword, no_scope=True),
            include('punct'),
            # if nothing else found, skip until end of line
            ('.*\\n', Text),
        ],
        'root': [
            # let's add strings here. there shouldn't be any root-level strings but you never know
            include('strings'),
            # skip whitespaces if indented line
            ("\\s+", Text),
            # macro has to be caught as soon as possible because of ambibuous syntax
            ("(?i)(\\w+)\\s*(\\(.*\\):\\s*)(MACRO)(\\s*=\\s*{)", bygroups(Name.Function, Text, Keyword, Text), 'macro'),
            ("(?i)(\\w+)\\s*(MACRO)(\\s*=\\s*{)", bygroups(Name.Function, Keyword, Text), 'macro'),
            # if stop appears in root, the rest of the file is unreachable
            ("\\s*(?i)\\b(stop|exit|quit)\\b\\s*;", Comment, 'stop'),
            # `root_cmds` is refactored out to be used in macro's body
            include('root_cmds'),
        ],
        'stop': [
            # if the stop command was nested, jump out of the `stop` scope at the end of the block
            # this is to prevent that a stop in an inactive branch disables highlighting for the rest of the file
            ('}', Text, '#pop'),
            #('\\n', Text),
            (".*\\n", Comment)
        ],
        'macro': [
            # let's add strings here. there shouldn't be any root-level strings but you never know
            include('strings'),
            # skip whitespaces if indented line
            ("\\s+", Text),
            ('}', Text, '#pop'),
            #("\\n", Punctuation, '#push'),
            include('root_cmds'),
            (".*?;", Text),
        ],
         'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        'exec': [
            ('\\w+', Name.Function),
            ('\\(', Text, "#pop"),
            (',\\s*', Text),
        ],
        'twiss': make_command(MAD_PROP_LIST),
        'option': make_command(MAD_OPTIONS),
        'set': make_command(["FORMAT", "SEQUENCE"]),
        'use': make_command(["SEQUENCE",
                             "PERIOD",
                             "SURVEY",
                             "RANGE",
                             ]),
        'select': make_command(["FLAG",
                                "RANGE",
                                "CLASS",
                                "PATTERN",
                                "SEQUENCE",
                                "FULL",
                                "CLEAR",
                                "COLUMN",
                                "SLICE",
                                "THICK",
                                "STEP",
                                "AT",
                                # flag options:
                                "SEQEDIT",
                                "ERROR",
                                "MAKETHIN",
                                "SECTORMAP",
                                "SAVE",
                                "INTERPOLATE",
                                "TWISS",
                             ]),
        'assign': make_command(["ECHO", "TRUNCATE"]),
        'call': make_command(["FILE"]),
        'print': make_command(["TEXT"]),
        'printf': make_command(["TEXT", "VALUE"]),
        'renamefile': make_command(["FILE", "TO"]),
        'copyfile': make_command(["FILE", "TO", "APPEND"]),
        'create': make_command(["TABLE", "COLUMN"]),
        'delete': make_command(["TABLE", "SEQUENCE"]),
        'readmytable': make_command(["TABLE", "FILE"]),
        'fill': make_command(["TABLE", "ROW"]),
        'setvars': make_command(["TABLE", "ROW", "KNOB", "CONST", "NOAPPEND"]),
        'fill_knob': make_command(["TABLE", "ROW", "KNOB", "SCALE"]),
        'setvars_lin': make_command(["TABLE", "ROW1", "ROW2", "PARAM"]),
        'beam': make_command([
            'particle', 'mass', 'charge',
            'energy', 'pc', 'gamma', 'beta', 'brho',
            'exn?', 'eyn?',
            'et', 'sig[te]',
            'kbunch', 'npart', 'bcurrent',
            'bunched', 'radiate', 'bv',
            'sequence',
            # particle options:
            'positron', 'electron', 'proton', 'antiproton', 'posmuon', 'negmuon', 'ion'
        ]),
        'resbeam': make_command(["sequence"]),
        'chdir': make_command(["dir"]),
        'seqedit': [
            include('strings'),
            ("ENDEDIT", Name.Class, '#pop'),
            (f'(?i)\\b(SEQUENCE)(\\s*=\\s*\\w+)?', bygroups(Name.Attribute, Text)),
            add_command('flatten', no_scope=True),
            add_command('reflect', no_scope=True),
            add_command('cycle'),
            add_command('install'),
            add_command('move'),
            add_command('remove'),
            add_command('replace'),
            include('punct'),
            ('.', Text),
            ("\\s+", Text),
        ],
        'cycle': make_command(["START"]),
        'install': make_command([
            "element", "class", "at", "from",
            "selected"
        ]),
        'move': make_command([
            "element", "by", "to", "from",
            "selected"
        ]),
        'remove': make_command([
            "element",
            "selected"
        ]),
        'replace': make_command([
            "element", "by",
            "selected"
        ]),
    }
