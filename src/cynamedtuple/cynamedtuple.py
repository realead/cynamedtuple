import cython


_TAB = "    "


def _create_members_definition(name_ctype_pairs):
    members = []
    for my_name, my_ctype in name_ctype_pairs:
        members.append(_TAB+"cdef public "+my_ctype+" "+my_name)
    return members


def _create_init_signature(names):
    return _TAB + "def __init__(self,"+", ".join(names)+"):"


def _create_init_body(names):
    inits = [_TAB+_TAB+"self."+x+" = "+x for x in names]
    return inits


def _ensure_as_pairs(name_types):
    if isinstance(name_types, dict):
        name_types = name_types.items()
    return name_types


def _create_cdef_class_code(classname, name_ctype_pairs):
    name_ctype_pairs = _ensure_as_pairs(name_ctype_pairs)
    names = [x[0] for x in name_ctype_pairs]
    code_lines = ["cdef class " + classname + ":"]
    code_lines.extend(_create_members_definition(name_ctype_pairs))
    code_lines.append(_create_init_signature(names))
    code_lines.extend(_create_init_body(names))
    return "\n".join(code_lines)+"\n"


def _create_cnamedtuple_class(classname, names):
    code = _create_cdef_class_code(classname, names)
    code = code + "GenericClass = " + classname +"\n"
    ret = cython.inline(code)
    return ret["GenericClass"]


def typed_namedtuple_cycode(class_name, fieldnames_with_types):
    """
    returns cython code which would be used to create the cdef-class
            names_with_types can be either an iterable of name-type pairs
                             or a dict
    """
    return _create_cdef_class_code(class_name, fieldnames_with_types)


def typed_namedtuple(class_name, fieldnames_with_types):
    """
    creates a typed named tuple with given class name and fields
            names_with_types can be either an iterable of name-type pairs
                             or a dict
    """
    return _create_cnamedtuple_class(class_name, fieldnames_with_types)
