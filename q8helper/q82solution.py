from bag import Bag
import unittest   #use unittest.TestCase
import random     #use random.shuffle, random.randint


class Test_Bag(unittest.TestCase):

    def setUp(self):
        self.test_list = ['d','a','b','d','c','b','d']
        self.bag = Bag(['d','a','b','d','c','b','d'])
        
    def testLen(self):
        self.assertEqual(len(self.bag), 7)
        removal = ['d','a','b','d','c','b','d']
        random.shuffle(removal)
        for r in range(len(removal)):
            self.bag.remove(removal[r])
            self.assertEqual(len(self.bag), 7-(r+1))
    def testUnique(self):
        self.setUp()
        self.assertEqual(self.bag.unique(),4)
        for i in self.test_list:
            self.bag.remove(i)
            self.test_list.remove(i)
            self.assertEqual(self.bag.unique(),len(set(self.test_list)))
    def testContains(self):
        self.setUp()
        self.assertTrue('a' in self.bag)
        self.assertTrue('b' in self.bag)
        self.assertTrue('c' in self.bag)
        self.assertTrue('d' in self.bag)
        self.assertFalse('x' in self.bag)
        
    def testCount(self):
        self.setUp()
        self.assertEqual(self.bag.count('a'),1)
        self.assertEqual(self.bag.count('b'),2)
        self.assertEqual(self.bag.count('c'),1)
        self.assertEqual(self.bag.count('d'),3)
        self.assertEqual(self.bag.count('x'),0)
        random.shuffle(self.test_list)
        for i in range(len(self.test_list)):
            self.bag.remove(self.test_list[i])
            sum_of_count = self.bag.count('a')+self.bag.count('b')+self.bag.count('c')+self.bag.count('d')
            self.assertEqual(sum_of_count, 7-(i+1))
    def testEqual(self):
        test_list = [random.randint(1,10) for i in range(1000)]
        test_bag1 = Bag(test_list)
        random.shuffle(test_list)
        test_bag2 = Bag(test_list)
        
        self.assertTrue(test_bag1==test_bag2)
        test_bag2.remove(test_list[0])
        self.assertFalse(test_bag1==test_bag2)
    def testAdd(self):
        test_list = [random.randint(1,10) for i in range(1000)]
        test_bag1 = Bag(test_list)
        test_bag2 = Bag()
        
        random.shuffle(test_list)
        for i in test_list:
            test_bag2.add(i)
        
            
        
        self.assertTrue(test_bag1==test_bag2)
        
    def testRemove(self):
        
        test_list = [random.randint(1,10) for i in range(1000)]
        test_bag1 = Bag(test_list)
        
        self.assertRaises(ValueError,test_bag1.remove, 21)
        
        test_bag2 = Bag(test_list)
        for i in test_list:
            test_bag2.add(i)
        for i in test_list:
            test_bag2.remove(i)
        
        self.assertEqual(test_bag1,test_bag2)
        
        
        
        
        
        
        
            
    
    

if __name__ == '__main__':
    unittest.main()

"""
Simple usage:

    import unittest

    class IntegerArithmeticTestCase(unittest.TestCase):
        def testAdd(self):  ## test method names begin 'test*'
            self.assertEqual((1 + 2), 3)
            self.assertEqual(0 + 1, 1)
        def testMultiply(self):
            self.assertEqual((0 * 10), 0)
            self.assertEqual((5 * 8), 40)

    if __name__ == '__main__':
        unittest.main()
"""