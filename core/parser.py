import re

from core.errors import OriginSyntaxError


token_spec = [
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('ID', r'[A-Za-z_]\w*'),
    ('OP', r'<=|>=|==|!=|[+\-*/=<>]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOL', r';'),
    ('COMMA', r','),
    ('SKIP', r'[ \t\n\r]+'),
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
    "to",
    "from",
    "end",
}


def parser(strings):
    tokens = []

    for line_num, line in enumerate(strings, 1):
        pos = 0
        while pos < len(line):
            match = None

            for tok_type, tok_regex in token_spec:
                regex = re.compile(tok_regex)
                m = regex.match(line, pos)

                if m:
                    text = m.group(0)
                    column = pos + 1

                    if tok_type == "ID":
                        if text in TYPES:
                            tokens.append(("TYPE", text, line_num, column))
                        elif text in COMMANDS:
                            tokens.append(("COMMAND", text, line_num, column))
                        else:
                            tokens.append(("ID", text, line_num, column))
                    elif tok_type != 'SKIP':
                        tokens.append((tok_type, text, line_num, column))

                    pos = m.end(0)
                    match = True
                    break

            if not match:
                # Якщо символ невідомий, ми тепер точно знаємо де він
                raise OriginSyntaxError(f"Невідомий символ: {line[pos]}", line=line_num, column=pos+1)

    return tokens
