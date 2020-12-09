import unittest

import cynamedtuple.cynamedtuple as t


class cynamedtupleTester(unittest.TestCase): 

   def test_test_me(self):
      self.assertEqual(t.test_me(), 42)
