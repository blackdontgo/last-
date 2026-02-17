#!/usr/bin/env python3
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(ROOT, 'images')
INDEX = os.path.join(ROOT, 'index.html')

def gather_files():
    names = []
    for n in os.listdir(IMG_DIR):
        # ignore hidden files
        if n.startswith('.'):
            continue
        names.append(n)
    names.sort(key=lambda s: s.lower())
    return names

def build_array(names):
    lines = ["const allMedia = [\n"]
    for i, n in enumerate(names):
        entry = "  'images/{}'".format(n.replace("'", "\\'"))
        if i != len(names) - 1:
            entry += ',\n'
        else:
            entry += '\n'
        lines.append(entry)
    lines.append('];\n')
    return ''.join(lines)

def replace_block(content, new_block):
    start = content.find('const allMedia = [')
    if start == -1:
        raise RuntimeError('allMedia block not found')
    # find matching closing bracket by scanning
    idx = start
    depth = 0
    found_start = False
    while idx < len(content):
        ch = content[idx]
        if content.startswith('const allMedia = [', idx):
            found_start = True
            # move to the '['
            idx = content.find('[', idx)
            depth = 1
            idx += 1
            break
        idx += 1
    if not found_start:
        raise RuntimeError('start not found')
    while idx < len(content):
        ch = content[idx]
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                end_idx = idx + 1
                # include following semicolon if present
                if end_idx < len(content) and content[end_idx] == ';':
                    end_idx += 1
                # replace from start to end_idx
                new_content = content[:start] + new_block + content[end_idx:]
                return new_content
        idx += 1
    raise RuntimeError('matching end not found')

def main():
    names = gather_files()
    new_block = build_array(names)
    with open(INDEX, 'r', encoding='utf-8') as f:
        content = f.read()
    updated = replace_block(content, new_block)
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(updated)
    print('Updated', INDEX, 'with', len(names), 'entries')

if __name__ == '__main__':
    main()
