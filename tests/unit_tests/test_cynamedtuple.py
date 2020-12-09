import unittest

from cynamedtuple import (
    typed_namedtuple_cycode,
    typed_namedtuple,
)


class CynamedtupleTester(unittest.TestCase): 
    def test_namedtuple_create_iter(self):
        A = typed_namedtuple("A", (("a", "int"), ("b", "long")))
        a = A(42, 21)
        self.assertEqual(a.a, 42)
        self.assertEqual(a.b, 21)

    def test_namedtuple_cycode(self):
        cycode = typed_namedtuple_cycode("AAA", (("a", "int"), ("b", "long")))
        self.assertTrue("cdef class AAA:" in cycode)
        self.assertTrue("cdef public int a" in cycode)
        self.assertTrue("cdef public long b" in cycode)

    def test_namedtuple_create_dict(self):
        A = typed_namedtuple("A", {"a": "int", "b": "long"})
        a = A(42, 21)
        self.assertEqual(a.a, 42)
        self.assertEqual(a.b, 21)
