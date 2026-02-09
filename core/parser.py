import re


token_spec = [
    ('NUMBER',    r'\d+'),
    ('STRING',    r'"[^"]*"'),
    ('ID',        r'[A-Za-z_]\w*'),
    ('OP',        r'<=|>=|==|!=|[+\-*/=<>]'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('SEMICOL',   r';'),
    ('COMMA',     r','),
    ('SKIP',      r'[ \t]+'),
    ('BACKSLASH', r'\\'),
]

TYPES = {"int", "str", "bool", "float"}  

COMMANDS = {
    "print",
    "if",
    "for",
    "else",
    "func",
    "start",
    "change",
    "type",
    "scan",
    "for",
    "to",
    "from",
    "end",
}

def parser(strings):
    tokens = []

    for line in strings:
        pos = 0
        while pos < len(line):
            match = None

            for tok_type, tok_regex in token_spec:
                regex = re.compile(tok_regex)
                m = regex.match(line, pos)

                if m:
                    text = m.group(0)

                    # 👇 ОСЬ ТУТ МАГІЯ
                    if tok_type == "ID":
                        if text in TYPES:
                            tokens.append(("TYPE", text))
                        elif text in COMMANDS:
                            tokens.append(("COMMAND", text))
                        else:
                            tokens.append(("ID", text))
                    elif tok_type not in ('SKIP', 'NEWLINE'):
                        tokens.append((tok_type, text))

                    pos = m.end(0)
                    match = True
                    break

            if not match:
                raise Exception(f"Невідомий символ: {line[pos]}")

    return tokens



