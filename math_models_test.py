import math_models_util as util
import math_models_population as population
import math_models_epidemic as epidemic
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

class TestMathModelsEpidemic(unittest.TestCase):
    def allEqual(self, tuple1, tuple2):
        return np.all(np.apply_along_axis(lambda x: x <= 0.0000001,
                                          0,
                                          np.abs(np.array(tuple1) - np.array(tuple2))))

    def testSIRModel(self):
        sir = epidemic.SIRModel(transmitRate=2.0, removeRate=0.75)
        self.assertTrue(self.allEqual(sir(sir.initialConditions, 0.1),
                                      (-0.0198, 0.0123, 0.0075)))
        self.assertTrue(self.allEqual(sir((0.9702, 0.0223, 0.0075), 0.2),
                                      (-0.0432709, 0.0265459, 0.016725)))
        self.assertTrue(self.allEqual(sir((0.926929080, 0.048845920, 0.024225), 0.3),
                                      (-0.0905534, 0.0539189, 0.0366344)))

    def testSEIRModel(self):
        seir = epidemic.SEIRModel(transmitRate=3.0, reducedEIRate=0.25, infectRate=1.0, removeRate=0.5)
        self.assertTrue(self.allEqual(seir(seir.initialConditions, 0.1),
                                      (-0.007425, -0.002575, 0.01, 0.0)))
        self.assertTrue(self.allEqual(seir((0.982575, 0.007425, 0.01, 0.0), 0.2),
                                      (-0.0349489, 0.0275239, 0.002425, 0.005)))
        self.assertTrue(self.allEqual(seir((0.9476261, 0.0349489, 0.012425, 0.005), 0.3),
                                      (-0.0601616, 0.0252127, 0.0287364, 0.0062125)))

if __name__ == "__main__":
    unittest.main()
