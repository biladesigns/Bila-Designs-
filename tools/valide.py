#!/usr/bin/env python3
"""Verifie l'imbrication des balises d'une page HTML."""
import re, sys
VOID = {'br','img','input','meta','link','hr','source','area','base','col','embed',
        'track','wbr','path','circle','rect','line','polyline','polygon','use','stop','ellipse'}
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.I | re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    pile, err = [], []
    for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*?(/?)>', s):
        ferm, tag, auto = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or auto or tag in ('!doctype',):
            continue
        if not ferm:
            pile.append(tag)
        elif pile and pile[-1] == tag:
            pile.pop()
        else:
            err.append((tag, pile[-3:]))
    ok = not pile and not err
    print(('  OK  ' if ok else '  KO  ') + f + ('' if ok else '  ouvertes=%s  orphelines=%s' % (pile[-4:], err[:3])))
