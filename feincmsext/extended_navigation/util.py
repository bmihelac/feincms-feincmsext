import re


def compile_expr(expr):
    """
    Compile expression ``expr``.

    Returns tuple of:

    * mapping
    * regex_lst
    * group_names

    >>> expr = "[image][caption]? / [section]{2}"
    >>> compile_expr(expr)
    ({'caption': 'B', 'image': 'A', 'section': 'C'}, ['[A][B]?', '[C]{2}'], [0, 1])
    """
    mapping = {} 
    regex_lst, group_names = [], []
    for index, s in enumerate(expr.split('/')):
        match = re.match(r'\<([^>]+)\>', s)
        if match:
            group_name = match.groups()[0]
            s = s.replace(match.group(), '')
        else:
            group_name = index
        for r in re.findall('\[\w+\]', s):
            name = r[1:-1]
            if name not in mapping.keys():
                char = chr(65 + len(mapping))
                mapping[name] = char
            else:
                char = mapping[name]
            s = s.replace(name, char)
        regex_lst.append(s.replace(' ', ''))
        group_names.append(group_name)
    return mapping, regex_lst, group_names
    
def regex_group_list(orig_lst, expr, get_type_func=None):
    """
    Group list items in `orig_lst` by expression `expr`.
    
    >>> lst = ['section', 'image', 'section', 'section']
    
    >>> expr = "[section]+" # group  sections together
    >>> regex_group_list(lst, expr)
    [(0, ['section']), (-1, ['image']), (0, ['section', 'section'])]

    >>> expr = "[section]{2}"
    >>> regex_group_list(lst, expr) # group 2 sections together
    [(-1, ['section', 'image']), (0, ['section', 'section'])]
    
    >>> lst = ['section', 'image', 'caption', 'image', 'section', 'section']
    >>> expr = "[image][caption]?" # group image and optionally caption
    >>> regex_group_list(lst, expr)
    [(-1, ['section']), (0, ['image', 'caption']), (0, ['image']), (-1, ['section', 'section'])]

    >>> lst = ['section', 'image', 'caption', 'image', 'section', 'section', 'section']
    >>> expr = "[image][caption]? / [section]{2}" # group every image with optionally caption, group all 2 successive sections
    >>> regex_group_list(lst, expr)
    [(-1, ['section']), (0, ['image', 'caption']), (0, ['image']), (1, ['section', 'section']), (-1, ['section'])]

    >>> lst = ['gif', 'jpg', 'txt', 'tiff', 'gif']
    >>> expr = "([gif]|[jpg]|[tiff])+" # group images
    >>> regex_group_list(lst, expr)
    [(0, ['gif', 'jpg']), (-1, ['txt']), (0, ['tiff', 'gif'])]

    >>> lst = ['A', 'start', 'B', 'C', 'end', 'D']
    >>> expr = "[start].*[end]" # group all between start and end
    >>> regex_group_list(lst, expr)
    [(-1, ['A']), (0, ['start', 'B', 'C', 'end']), (-1, ['D'])]

    >>> lst = ['gif', 'jpg', 'txt', 'tiff', 'gif']
    >>> expr = "<images>([gif]|[jpg]|[tiff])+" # named groups
    >>> regex_group_list(lst, expr)
    [('images', ['gif', 'jpg']), (-1, ['txt']), ('images', ['tiff', 'gif'])]
    """
    
    if not get_type_func:
        get_type_func = lambda x: x
    mapping, regex_lst, group_names = compile_expr(expr)
    s = ''.join([mapping.get(get_type_func(e), '9') for e in orig_lst])
    groups = {}
    for regex, group_name in zip(regex_lst, group_names):
        for result in re.finditer(regex, s):
            start, end = result.start(), result.end()
            groups[start] = (group_name, orig_lst[start:end])
            s = s[:start] + '0'*(end-start) + s[end:]
    for result in re.finditer('[^0]+', s):
        start, end = result.start(), result.end()
        groups[start] = (-1, orig_lst[start:end])
    return [groups[key] for key in sorted(groups.iterkeys())]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
