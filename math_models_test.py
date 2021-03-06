import unittest
import numpy as np
import math_models_util as util
import math_models_population as population
import math_models_epidemic as epidemic

def fequal(lhs, rhs):
    return np.abs(lhs - rhs) <= 0.0000001

def tequal(tuple1, tuple2):
    for lhs, rhs in zip(tuple1, tuple2):
        if not fequal(lhs, rhs):
            return False
    return True

class TestMathModelsUtil(unittest.TestCase):
    def testPolyChangeFtnIncreasing(self):
        pc = util.PolyChangeFtn(1, 1)
        self.assertTrue(fequal(pc(0), 0))
        self.assertTrue(fequal(pc(1), 0.5))
        self.assertTrue(fequal(pc(2), 0.6666666))
        self.assertTrue(fequal(pc(3), 0.75))
        self.assertTrue(fequal(pc(4), 0.80))
        self.assertTrue(fequal(pc(5), 0.8333333))
        self.assertTrue(pc(10) <= 1.0)
        self.assertTrue(pc(50) <= 1.0)
        self.assertTrue(pc(100) <= 1.0)
        self.assertTrue(pc(500) <= 1.0)
        self.assertTrue(pc(1000) <= 1.0)

    def testPolyChangeFtnIncreasing2(self):
        pc = util.PolyChangeFtn(0.2, 10)
        self.assertTrue(fequal(pc(0), 0))
        self.assertTrue(fequal(pc(1), 0.0181818))
        self.assertTrue(fequal(pc(10), 0.1))
        self.assertTrue(fequal(pc(50), 0.1666666))
        self.assertTrue(fequal(pc(100), 0.1818181))
        self.assertTrue(fequal(pc(500), 0.1960784))
        self.assertTrue(fequal(pc(1000), 0.1980198))
        self.assertTrue(pc(5000) <= 0.2)
        self.assertTrue(pc(10000) <= 0.2)

    def testPolyChangeFtnDecreasing(self):
        pc = util.PolyChangeFtn(-1, 1)
        self.assertTrue(fequal(pc(0), 0))
        self.assertTrue(fequal(pc(1), -0.5))
        self.assertTrue(fequal(pc(2), -0.6666666))
        self.assertTrue(fequal(pc(3), -0.75))
        self.assertTrue(fequal(pc(4), -0.80))
        self.assertTrue(fequal(pc(5), -0.8333333))
        self.assertTrue(pc(10) >= -1.0)
        self.assertTrue(pc(50) >= -1.0)
        self.assertTrue(pc(100) >= -1.0)
        self.assertTrue(pc(500) >= -1.0)
        self.assertTrue(pc(1000) >= -1.0)

    def testPolyChangeFtnDecreasing2(self):
        pc = util.PolyChangeFtn(-0.2, 10)
        self.assertTrue(fequal(pc(0), 0))
        self.assertTrue(fequal(pc(1), -0.0181818))
        self.assertTrue(fequal(pc(10), -0.1))
        self.assertTrue(fequal(pc(50), -0.1666666))
        self.assertTrue(fequal(pc(100), -0.1818181))
        self.assertTrue(fequal(pc(500), -0.1960784))
        self.assertTrue(fequal(pc(1000), -0.1980198))
        self.assertTrue(pc(5000) >= -0.2)
        self.assertTrue(pc(10000) >= -0.2)

    def testExpChangeFtnIncreasing(self):
        ec = util.ExpChangeFtn(1, 1)
        self.assertTrue(fequal(ec(0), 0))
        self.assertTrue(fequal(ec(1), 0.6321205))
        self.assertTrue(fequal(ec(2), 0.8646647))
        self.assertTrue(fequal(ec(3), 0.9502129))
        self.assertTrue(fequal(ec(4), 0.9816843))
        self.assertTrue(fequal(ec(5), 0.993262))
        self.assertTrue(ec(10) <= 1.0)
        self.assertTrue(ec(50) <= 1.0)
        self.assertTrue(ec(100) <= 1.0)
        self.assertTrue(ec(500) <= 1.0)
        self.assertTrue(ec(1000) <= 1.0)

    def testExpChangeFtnIncreasing2(self):
        ec = util.ExpChangeFtn(0.2, 10)
        self.assertTrue(fequal(ec(0), 0))
        self.assertTrue(fequal(ec(10), 0.1264241))
        self.assertTrue(fequal(ec(25), 0.183583))
        self.assertTrue(fequal(ec(50), 0.1986524))
        self.assertTrue(fequal(ec(100), 0.1999909))
        self.assertTrue(fequal(ec(200), 0.1999999))
        self.assertTrue(ec(1000) <= 2.0)
        self.assertTrue(ec(10000) <= 2.0)

    def testExpChangeFtnDecreasing(self):
        ec = util.ExpChangeFtn(-1, 1)
        self.assertTrue(fequal(ec(0), 0))
        self.assertTrue(fequal(ec(1), -0.6321205))
        self.assertTrue(fequal(ec(2), -0.8646647))
        self.assertTrue(fequal(ec(3), -0.9502129))
        self.assertTrue(fequal(ec(4), -0.9816843))
        self.assertTrue(fequal(ec(5), -0.993262))
        self.assertTrue(ec(10) >= -1.0)
        self.assertTrue(ec(50) >= -1.0)
        self.assertTrue(ec(100) >= -1.0)
        self.assertTrue(ec(500) >= -1.0)
        self.assertTrue(ec(1000) >= -1.0)

    def testExpChangeFtnDecreasing2(self):
        ec = util.ExpChangeFtn(-0.2, 10)
        self.assertTrue(fequal(ec(0), 0))
        self.assertTrue(fequal(ec(10), -0.1264241))
        self.assertTrue(fequal(ec(25), -0.183583))
        self.assertTrue(fequal(ec(50), -0.1986524))
        self.assertTrue(fequal(ec(100), -0.1999909))
        self.assertTrue(fequal(ec(200), -0.1999999))
        self.assertTrue(ec(1000) >= -2.0)
        self.assertTrue(ec(10000) >= -2.0)

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

    def testXYsMinMaxRange(self):
        mmr = util.XYsMinMaxRange([1, 2, 3], [[1.0, 2.0, 4.0], [-1.0, 0.0, 1.0]])
        self.assertEqual(mmr.xMin, 1)
        self.assertEqual(mmr.xMax, 3)
        self.assertEqual(mmr.yMin, -1.0)
        self.assertEqual(mmr.yMax, 4.0)
        self.assertEqual(mmr.deltaPct, 0.05)
        self.assertEqual(mmr.xRange(), (0.95, 3.05))
        self.assertEqual(mmr.yRange(), (-1.05, 4.05))

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
    def testCompartmentModelBase(self):
        cm = epidemic.CompartmentModelBase(initialConditions=(1, 0, 0),
                                           labels=['A', 'B', 'C'],
                                           colors=['r', 'b', 'g'])
        self.assertEqual(cm.numCompartments, 3)
        self.assertEqual(cm.initialConditions, (1, 0, 0))
        self.assertEqual(cm.labels, ['A', 'B', 'C'])
        self.assertEqual(cm.colors, ['r', 'b', 'g'])
        self.assertTrue(cm.hasLabel('A'))
        self.assertTrue(cm.hasLabel('B'))
        self.assertTrue(cm.hasLabel('C'))
        self.assertFalse(cm.hasLabel('D'))
        self.assertTrue(cm.hasColor('r'))
        self.assertTrue(cm.hasColor('b'))
        self.assertTrue(cm.hasColor('g'))
        self.assertFalse(cm.hasColor('c'))
        self.assertEqual(cm.labelColor('A'), 'r')
        self.assertEqual(cm.labelColor('B'), 'b')
        self.assertEqual(cm.labelColor('C'), 'g')

    def testSIRModel(self):
        sir = epidemic.SIRModel(transmitRate=2.0, removeRate=0.75)
        self.assertTrue(tequal(sir(sir.initialConditions, 0.1),
                               (-0.0198, 0.0123, 0.0075)))
        self.assertTrue(tequal(sir((0.9702, 0.0223, 0.0075), 0.2),
                               (-0.0432709, 0.0265459, 0.016725)))
        self.assertTrue(tequal(sir((0.926929080, 0.048845920, 0.024225), 0.3),
                               (-0.0905534, 0.0539189, 0.0366344)))

    def testSEIRModel(self):
        seir = epidemic.SEIRModel(transmitRate=3.0,
                                  reducedEIRate=0.25,
                                  infectRate=1.0,
                                  removeRate=0.5)
        self.assertTrue(tequal(seir(seir.initialConditions, 0.1),
                               (-0.007425, -0.002575, 0.01, 0.0)))
        self.assertTrue(tequal(seir((0.982575, 0.007425, 0.01, 0.0), 0.2),
                               (-0.0349489, 0.0275239, 0.002425, 0.005)))
        self.assertTrue(tequal(seir((0.9476261, 0.0349489, 0.012425, 0.005), 0.3),
                               (-0.0601616, 0.0252127, 0.0287364, 0.0062125)))

if __name__ == "__main__":
    unittest.main()
