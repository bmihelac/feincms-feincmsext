import re

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
    """
    
    def compile_expr(expr):
        mapping = {} 
        regex_lst = []
        for s in expr.split('/'):
            for r in re.findall('\[\w+\]', s):
                name = r[1:-1]
                if name not in mapping.keys():
                    char = chr(65 + len(mapping))
                    mapping[name] = char
                else:
                    char = mapping[name]
                s = s.replace(name, char)
            regex_lst.append(s.replace(' ', ''))
        return mapping, regex_lst    
    
    if not get_type_func:
        get_type_func = lambda x: x
    mapping, regex_lst = compile_expr(expr)
    # transform orig_lst items to one char, giving 1st expression 'A',
    # 2nd 'B' and so on. If orig_lst item has no mapping mark it with '9'
    s = ''.join([mapping.get(get_type_func(e), '9') for e in orig_lst])
    groups = {}
    for i, regex in enumerate(regex_lst):
        for result in re.finditer(regex, s):
            start, end = result.start(), result.end()
            groups[start] = (i, orig_lst[start:end])
            s = s[:start] + '0'*(end-start) + s[end:]
    for result in re.finditer('[^0]+', s):
        start, end = result.start(), result.end()
        groups[start] = (-1, orig_lst[start:end])
    return [groups[key] for key in sorted(groups.iterkeys())]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
