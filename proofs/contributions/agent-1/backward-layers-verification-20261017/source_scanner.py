def lean_code_tokens(source):
    """Mask nested Lean comments and string contents before the auxiliary scan."""
    out, i, depth = [], 0, 0
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                depth += 1
                out.extend('  ')
                i += 2
            elif source.startswith('-/', i):
                depth -= 1
                out.extend('  ')
                i += 2
            else:
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif source.startswith('/-', i):
            depth = 1
            out.extend('  ')
            i += 2
        elif source.startswith('--', i):
            j = source.find('\n', i)
            j = len(source) if j == -1 else j
            out.extend(' ' * (j - i))
            i = j
        elif source[i] == '"':
            out.append(' ')
            i += 1
            while i < len(source):
                ch = source[i]
                out.append('\n' if ch == '\n' else ' ')
                i += 1
                if ch == '\\' and i < len(source):
                    out.append('\n' if source[i] == '\n' else ' ')
                    i += 1
                elif ch == '"':
                    break
            else:
                raise AssertionError('Unterminated Lean string in source scan')
        else:
            out.append(source[i])
            i += 1
    assert depth == 0, 'Unterminated Lean block comment in source scan'
    return ''.join(out)

