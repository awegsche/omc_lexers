from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

# options, following the pattern
# ```
# option, flag;
# ```
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

# built-in mathematical functions
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

# control flow keywords
MAD_KEYWORD = [
    "IF",
    "ELSE",
    "ELSEIF",
    "WHILE",
    "TRUE",
    "FALSE",
]

# most madx commands follow the structure
# ```
# COMMAND, BOOL_FLAG, VALUE_FLAG=value;
# ```
# the following two functions register those commands and their respective scope
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
        (f'(?i)\\b({"|".join(attrs)})(\\s*:?=\\s*[^,;]+)?', bygroups(Name.Attribute, Text)),
        include('punct'),
        ('.', Text),
        #(r'[^;]', Text),
    ]

# MADX accelerator elements are defined as
# ```
# label: TYPE, attrs;
# ```
# the following two functions register those element definitions and their respective scope
def add_element(name, no_scope=False, scope_name=None, token=Name.Class, aliases=None):
    if scope_name is None:
        scope_name = name
    matcher = name
    if aliases is not None:
        matcher = f"{'|'.join(aliases)}"
    if no_scope:
        return (f"(\\w+)(\\s*:\\s*)(?i)({matcher})", bygroups(Name.Variable, Text, token))
    return (f"(\\w+)(\\s*:\\s*)(?i)({matcher})", bygroups(Name.Variable, Text, token), scope_name)

def make_element(attrs):
    return [
        include('strings'),
        (';', Text, '#pop'),
        (f'(\\s*)(?i)({"|".join(attrs)})(\\s*:?=\\s*[^,;]+)', bygroups(Text, Name.Attribute, Text)),
        (',', Text),
        ('[^,;]+', Text),
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
            ("\\s*[+\\-*\\/]\\s*", Operator),
            ("\\s*[><]=?\\s*", Operator),
            ("\\s*:?=\\s*", Operator),
            ("=", Operator),
        ],
        'root_cmds': [
            # general fall back highlighting, will vanish over time
            (f'(?i)\\b({"|".join(MADX_BUILTIN_FN)})(\\()', bygroups(Name.Class, Text)),
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
            add_command('twiss'),

            # element definitions
            add_element('marker', no_scope=True),
            add_element('rbend'),
            add_element('drift'),
            add_element('sbend'),
            add_element('rbend'),
            add_element('dipedge'),
            add_element('quadrupole'),
            add_element('sextupole'),
            add_element('octupole'),
            add_element('multipole'),
            add_element('solenoid'),
            add_element('nllens'),
            add_element('[hv]kicker', scope_name="hvkicker"),
            add_element('kicker'),
            add_element('save_state'),
            add_element('rfcavity'),
            add_element('twcavity'),
            add_element('crabcavity'),
            add_element('rfmultipole'),
            add_element('[hv]acdipole', scope_name="hvacdipole"),
            add_element('elseparator'),
            add_element('monitor', scope_name="monitor", aliases=["[hv]?monitor", "instrument", "placeholder"]),
            add_element('collimator'),
            add_element('[er]collimator', scope_name="ercollimator"),
            add_element('beambeam'),
            add_element('matrix'),
            add_element('[xys]rotation', scope_name="rotation"),
            add_element('translation'),
            # for everything else that matches the assignment pattern:
            add_element('\\w+', no_scope=True, token=Name.Variable),
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
            ('.*?\\)', Text),
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
            ("\\s*(?i)\\b(stop|exit|quit|return)\\b\\s*;", Comment, 'stop'),
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
        'twiss': make_command([
            "SEQUENCE", "LINE", "RANGE",
            "DELTAP",
            "CHROM",
            "CENTRE", "TOLERANCE",
            "FILE",
            "(NO)?TABLE",
            "RMATRIX", "SECTORMAP",
            "SECTORTABLE", "SECTORFILE",
            "SECTORPURE",
            "EIGENVECTOR", "EIGENFILE",
            "KEEPORBIT", "USEORBIT",
            "COUPLE", "EXACT",
            "RIPKEN", "TAPERING"
        ]),
        # elements ---------------------------------------------------------------------------------
        'rbend': make_element([
            "L", "ANGLE", "TILT",
            "K[012]S?", "E[12]", "FINTX?",
            "HGAP", "H[12]", "THICK", "ADD_ANGLE", "KILL_ENT_FRINGE"
        ]),
        'sbend': make_element([
            "L", "ANGLE", "TILT",
            "K[01]S?", "E[12]", "FINTX?",
            "HGAP", "H[12]", "THICK", "KILL_ENT_FRINGE"
        ]),
        'drift': make_element([
            "L"
        ]),
        'dipedge': make_element([
            "H", "E1", "FINT", "HGAP", "TILT"
        ]),
        'quadrupole': make_element([
            "L", "K1S?", "TILT", "THICK"
        ]),
        'sextupole': make_element([
            "L", "K2S?", "TILT"
        ]),
        'octupole': make_element([
            "L", "K3S?", "TILT"
        ]),
        'multipole': make_element([
            "LRAD", "K[NS]L", "TILT"
        ]),
        'solenoid': make_element([
            "L", "KSI?"
        ]),
        'nllens': make_element([
            "[KC]NLL"
        ]),
        'hvkicker': make_element([
            "L", "TILT",
            #"(?>SIN)?KICK",
            #"SIN(?>TUNE|PEAK|PHASE)"
            "SINKICK", "KICK", "SINTUNE", "SINPEAK", "SINPHASE"
        ]),
        'kicker': make_element([
            "L", "[HV]KICK", "TILT"
        ]),
        'rfcavity': make_element([
            "L", "VOLT", "LAG", "FREQ", "HARMON", "N_BESSEL", "NO_CAVITY_TOTALPATH"
        ]),
        'twcavity': make_element([
            "L", "VOLT", "LAG", "FREQ", "PSI", "DELTA_LAG"
        ]),
        'crabcavity': make_element([
            "L", "VOLT", "LAG", "FREQ", "HARMON",
            "RV[1234]", "RPH[12]", "LAGF"
        ]),
        'hvacdipole': make_element([
            "L", "VOLT", "LAG", "FREQ"
            "RAMP[1234]"
        ]),
        'rfmultipole': make_element([
            "L", "VOLT", "LAG", "FREQ", "HARMON",
            "LRAD", "TILT",
            "[KP][NS]L"
        ]),
        'save_state': make_element([
            "SEQUENCE", "FILE", "BEAM", "FOLDER", "CSAVE"
        ]),
        'elseparator': make_element([
            "L", "E[XY]", "TILT"
        ]),
        'monitor': make_element([
            "L"
        ]),
        'collimator': make_element([
            "L",
            #"APER(?>_(?>OFFSET|TOL)|(?>URE|YPE))"
            "APERTURE", "APEROFFSET", "APERTOL", "APTERTYPE"
        ]),
        'ercollimator': make_element([
            "L", "[XY]SIZE"
        ]),
        'beambeam': make_element([
            "CHARGE", "[XY]MA", "SIG[XY]", "WIDTH",
            #"BB(?>SHAPE|DIR)"
            "BBSHAPE", "BBDIR"
        ]),
        'matrix': make_element([
            "TYPE", "L", "KICK[1-6]", "RM[1-6][1-6]", "TM[1-6][1-6][1-6]"
        ]),
        'rotation': make_element([
            "ANGLE"
        ]),
        'translation': make_element([
            "D[XYS]"
        ]),
    }
