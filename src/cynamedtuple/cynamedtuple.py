import cython
import itertools


_TAB = "    "


def _create_members_definition(name_ctype_pairs):
    members = []
    for my_name, my_ctype in name_ctype_pairs:
        members.append(_TAB+"cdef public "+my_ctype+" "+my_name)
    return members


def _create_init_signature(names, defaults):
    as_str = ["="+str(d) for d in defaults]
    len_diff = len(names)-len(as_str)
    if len_diff<0:
        raise TypeError("Got more default values than field names")
    args = zip(names,  [""]*len_diff + as_str)
    all_args = ", ".join(x[0]+x[1] for x in args)
    return _TAB + "def __init__(self,"+all_args+"):"


def _create_init_body(names):
    inits = [_TAB*2+"self."+x+" = "+x for x in names]
    return inits


def _create_getitem(names):
    code = [_TAB + "def __getitem__(self, i):"]
    n = len(names)
    for i, name in enumerate(names):
        line = "if i=={pos} or i=={neg}: return self.{name}".format(pos=i, neg=-n+i, name=name)
        code.append(_TAB*2+line)
    code.append(_TAB*2+"raise IndexError('tuple index out of range')")
    return code

def _ensure_as_pairs(name_types):
    if isinstance(name_types, dict):
        name_types = name_types.items()
    return list(name_types)


def _create_cdef_class_code(classname, name_ctype_pairs, defaults, cython_header):
    name_ctype_pairs = _ensure_as_pairs(name_ctype_pairs)
    names = [x[0] for x in name_ctype_pairs]
    code_lines = []
    code_lines.extend(cython_header)
    code_lines.append("cdef class " + classname + ":")
    code_lines.extend(_create_members_definition(name_ctype_pairs))
    code_lines.append(_create_init_signature(names, defaults))
    code_lines.extend(_create_init_body(names))
    code_lines.extend(_create_getitem(names))
    return "\n".join(code_lines)+"\n"


def _create_cnamedtuple_class(classname, code, cython_options):
    code = code + "\nGenericClass = " + classname +"\n"
    ret = cython.inline(code, **cython_options)
    return ret["GenericClass"]


def typed_namedtuple_cycode(class_name, fieldnames_with_types, *, defaults=[], cython_header=[]):
    """
    returns cython code which would be used to create Cython's cdef-class
            fieldnames_with_types can be either an iterable of name-type pairs
                                  or a dict
            defaults      - default values for fields
            cython_header - cimports, cdeftypes and similar Cython definitons,
                            which should be imported before cdef-class definition
    """
    return _create_cdef_class_code(class_name, fieldnames_with_types, defaults, cython_header)


def typed_namedtuple(class_name, fieldnames_with_types, *, defaults=[], cython_options = {'quiet':True}):
    """
    creates a typed named tuple with given class name and fields
            fieldnames_with_types can be either an iterable of name-type pairs
                                  or a dict
            defaults      - default values for fields
            cython_options - options for cython-build

    Usage:

    >>> MyStruct = typed_namedtuple("MyStruct", dict(a="int", b="int", c="int"), defaults=[2,3])
    >>> s = MyStruct(5)
    >>> s.a, s.b, s.c
    (5, 2, 3)
    >>> s[0], s[1], s[-1]
    (5, 2, 3)

    """
    code = typed_namedtuple_cycode(class_name, fieldnames_with_types, defaults=defaults)
    return _create_cnamedtuple_class(class_name, code, cython_options)


def untyped_namedtuple_cycode(class_name, fieldnames, *, defaults=[]):
    """
    returns cython code which would be used to create Cython's cdef-class
            fieldnames    - names of fields
            defaults      - default values for fields
    """
    fieldnames_with_types = zip(fieldnames, itertools.repeat("object"))
    return typed_namedtuple_cycode(class_name, fieldnames_with_types, defaults=defaults)


def untyped_namedtuple(class_name, fieldnames, *, defaults=[], cython_options = {'quiet':True}):
    """
    creates a typed named tuple with given class name and fields
            fieldnames_with_types can be either an iterable of name-type pairs
                                  or a dict
            defaults      - default values for field names
            cython_options - options for cython-build
    Usage:

    >>> MyStruct = untyped_namedtuple("MyStruct", ["a", "b", "c"], defaults=[2,3])
    >>> s = MyStruct(5)
    >>> s.a, s.b, s.c
    (5, 2, 3)
    >>> s[0], s[1], s[-1]
    (5, 2, 3)

    """
    code = untyped_namedtuple_cycode(class_name, fieldnames, defaults=defaults)
    return _create_cnamedtuple_class(class_name, code, cython_options)
