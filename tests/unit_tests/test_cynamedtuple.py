import unittest

from cynamedtuple import (
    typed_namedtuple_cycode,
    typed_namedtuple,
    untyped_namedtuple_cycode,
    untyped_namedtuple,
)


class CynamedtupleTester(unittest.TestCase): 
    def test_typed_namedtuple_create_iter(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "long")))
        a = A(42, 21)
        self.assertEqual(a.a, 42)
        self.assertEqual(a.b, 21)

    def test_typed_namedtuple_cycode(self):
        cycode = typed_namedtuple_cycode("AAA", (("a", "int"), ("b", "long")))
        self.assertTrue("cdef class AAA:" in cycode, msg=cycode)
        self.assertTrue("cdef public int a" in cycode, msg=cycode)
        self.assertTrue("cdef public long b" in cycode, msg=cycode)

    def test_typed_namedtuple_create_dict(self):
        A = typed_namedtuple("A", {"a": "int", "b": "long"})
        a = A(42, 21)
        self.assertEqual(a.a, 42)
        self.assertEqual(a.b, 21)

    def test_typed_namedtuple_getitem_positive(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")))
        a = A(1,2,3)
        self.assertEqual(a[0], 1)
        self.assertEqual(a[1], 2)
        self.assertEqual(a[2], 3)
        with self.assertRaises(IndexError) as context:
            a[3]
        self.assertEqual("tuple index out of range", context.exception.args[0])

    def test_typed_namedtuple_getitem_negative(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")))
        a = A(1,2,3)
        self.assertEqual(a[-1], 3)
        self.assertEqual(a[-2], 2)
        self.assertEqual(a[-3], 1)
        with self.assertRaises(IndexError) as context:
            a[-4]
        self.assertEqual("tuple index out of range", context.exception.args[0])

    def test_typed_namedtuple_all_defaults(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")), defaults=[1,2,3])
        a = A()
        self.assertEqual(a.a, 1)
        self.assertEqual(a.b, 2)
        self.assertEqual(a.c, 3)

    def test_typed_namedtuple_last_defaults(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")), defaults=[2,3])
        a = A(5)
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, 2)
        self.assertEqual(a.c, 3)

    def test_typed_namedtuple_last_defaults_overwritten(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")), defaults=[2,3])
        a = A(5,44)
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, 44)
        self.assertEqual(a.c, 3)

    def test_typed_namedtuple_too_many_defaults(self):
        with self.assertRaises(TypeError) as context:
            typed_namedtuple("A", (("a", "int"), ("b", "int"), ("c", "int")), defaults=[1,0,2,3])
        self.assertEqual("Got more default values than field names", context.exception.args[0])

    def test_typed_namedtuple_cython_header(self):
        cycode = typed_namedtuple_cycode("A", (("a", "myint"),), cython_header = ["ctypedef int myint"])
        header = cycode.find("ctypedef int myint\n")
        classdef = cycode.find("cdef class A:\n")
        self.assertTrue(header>=0)
        self.assertTrue(classdef>=0)
        self.assertTrue(header<classdef)

    def test_untyped_namedtuple_cycode(self):
        cycode = untyped_namedtuple_cycode("BBB", ("a", "b"))
        self.assertTrue("cdef class BBB:" in cycode, msg=cycode)
        self.assertTrue("cdef public object a" in cycode, msg=cycode)
        self.assertTrue("cdef public object b" in cycode, msg=cycode)

    def test_untyped_namedtuple_create(self):
        A = untyped_namedtuple("A", ("a", "b"))
        a = A(42, 21)
        self.assertEqual(a.a, 42)
        self.assertEqual(a.b, 21)

    def test_untyped_namedtuple_getitem_positive(self):
        A = untyped_namedtuple("A", ("a", "b", "c"))
        a = A(1,2,3)
        self.assertEqual(a[0], 1)
        self.assertEqual(a[1], 2)
        self.assertEqual(a[2], 3)
        with self.assertRaises(IndexError) as context:
            a[3]
        self.assertEqual("tuple index out of range", context.exception.args[0])

    def test_untyped_namedtuple_getitem_negative(self):
        A = untyped_namedtuple("A", ("a", "b", "c"))
        a = A(1,2,3)
        self.assertEqual(a[-1], 3)
        self.assertEqual(a[-2], 2)
        self.assertEqual(a[-3], 1)
        with self.assertRaises(IndexError) as context:
            a[-4]
        self.assertEqual("tuple index out of range", context.exception.args[0])

    def test_untyped_namedtuple_all_defaults(self):
        A = untyped_namedtuple("A", ("a", "b", "c"), defaults=[1,2,3])
        a = A()
        self.assertEqual(a.a, 1)
        self.assertEqual(a.b, 2)
        self.assertEqual(a.c, 3)

    def test_untyped_namedtuple_last_defaults(self):
        A = untyped_namedtuple("A", ("a", "b", "c"), defaults=[2,3])
        a = A(5)
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, 2)
        self.assertEqual(a.c, 3)

    def test_untyped_namedtuple_last_defaults_overwritten(self):
        A = untyped_namedtuple("A", ("a", "b", "c"), defaults=[2,3])
        a = A(5,"44")
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, "44")
        self.assertEqual(a.c, 3)

    def test_untyped_namedtuple_too_many_defaults(self):
        with self.assertRaises(TypeError) as context:
            untyped_namedtuple("A", ("a", "b", "c"), defaults=[1,0,2,3])
        self.assertEqual("Got more default values than field names", context.exception.args[0])
