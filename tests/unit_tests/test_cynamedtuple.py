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
