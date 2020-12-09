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
