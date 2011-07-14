def escape_csv(data):
    if '"' in data:
        return '"%s"' % data.replace('"', '""')
    else:
        return data

def unescape_csv(data):
    if '"' in data:
        return data[1:-1].replace('""', '"')
    else:
        return data

def test():
    escaped = [
            "No quotes",
            "'Single quotes'",
            "\"test \"\"a\"\" test\"",
            "\"\"\"\"",
            ]

    unescaped = [
            "No quotes",
            "'Single quotes'",
            "test \"a\" test",
            "\"",
            ]

    assert([escape_csv(data) for data in unescaped] == escaped)
    assert([unescape_csv(data) for data in escaped] == unescaped)

if __name__ == '__main__':
    test()
