import math_models_util as util
import math_models_population as population
import numpy as np
import unittest

class TestMathModelsUtil(unittest.TestCase):
    def testSumCallablesFtn(self):
        sc = util.SumCallablesFtn([lambda x: 2 * x, lambda x: x, lambda x: x - 1])
        self.assertEqual(sc(-5), -21)
        self.assertEqual(sc(-1), -5)
        self.assertEqual(sc(0), -1)
        self.assertEqual(sc(1), 3)
        self.assertEqual(sc(5), 19)

    def testMinCallablesFtn(self):
        sc = util.MinCallablesFtn([lambda x: 2 * x, lambda x: x, lambda x: x - 1])
        self.assertEqual(sc(-5), -10)
        self.assertEqual(sc(-1), -2)
        self.assertEqual(sc(0), -1)
        self.assertEqual(sc(1), 0)
        self.assertEqual(sc(5), 4)

    def testPiecewiseFtn(self):
        pw = util.PiecewiseFtn([-1, 0, 1], [-10, -5, 5, 10])
        self.assertEqual(pw(-2), -10)
        self.assertEqual(pw(-1), -10)
        self.assertEqual(pw(-0.5), -5)
        self.assertEqual(pw(0), -5)
        self.assertEqual(pw(0.5), 5)
        self.assertEqual(pw(1), 5)
        self.assertEqual(pw(2), 10)

    def testFunctionPoints(self):
        fp = util.FunctionPoints(lambda x: 2 * x, np.array([1, 4, 3, 5, 2]))
        self.assertTrue(np.all(fp.y == np.array([2, 8, 6, 10, 4])))
        self.assertEqual(fp.yMin, 2)
        self.assertEqual(fp.yMax, 10)
        self.assertTrue(np.all(fp.minLine() == np.array([2, 2, 2, 2, 2])))
        self.assertTrue(np.all(fp.maxLine() == np.array([10, 10, 10, 10, 10])))

class TestMathModelsPopulation(unittest.TestCase):
    def testDimension(self):
        dim = population.Dimension('foobar',
                                   [lambda x: x + 5, lambda x: 2 * x, lambda x: x])
        self.assertEqual(dim(0), 5)
        self.assertEqual(dim(1), 9)
        self.assertEqual(dim(5), 25)

    def testCarryingCapacity(self):
        cc = population.CarryingCapacity(
            1000000,
            [population.Dimension(
                'Dim1',
                [lambda x: 0.1 * x,
                 lambda x: 0.2 * x,
                 lambda x: -0.05 * x]),
             population.Dimension(
                 'Dim2',
                 [lambda x: 0.1 * x,
                  lambda x: 0.3 * x,
                  lambda x: -0.02 * x])])
        self.assertEqual(cc(0), 1000000)
        self.assertEqual(cc(1), 1250000)
        self.assertEqual(cc(2), 1500000)

    def testLogisticModel(self):
        lm = population.LogisticModel(
            0.05,
            100000,
            population.CarryingCapacity(
                1000000,
                [population.Dimension(
                    'Dim1',
                    [lambda x: 0.1 * x, lambda x: -0.05 * x]),
                 population.Dimension(
                    'Dim2',
                    [lambda x: 0.2 * x, lambda x: -0.1 * x])]))
        self.assertEqual(int(lm(10000, 0)), 495)
        self.assertEqual(int(lm(10495, 1)), 519)
        self.assertEqual(int(lm(11014, 2)), 545)

if __name__ == "__main__":
    unittest.main()
