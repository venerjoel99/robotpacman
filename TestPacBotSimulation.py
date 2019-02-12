import PacBotSimulation
import unittest

class TestPosition(unittest.TestCase):

    def __init__(self, *args, **argw):
        super(TestPosition, self).__init__(*args, **argw)

    def test_construction(self):
        position1 = PacBotSimulation.Position(10, 3)
        position2 = PacBotSimulation.Position(3,3)

    def test_getX(self):
        position1 = PacBotSimulation.Position(10, 3)
        
        xVal = position1.getX()

        self.assertEqual(xVal, 10)
        self.assertEqual(position1.x, 10)
        self.assertEqual(position1.y, 3)
    
    def test_getY(self):
        position1 = PacBotSimulation.Position(10, 3)

        yVal = position1.getY()

        self.assertEqual(yVal, position1.getY(), 3)
        self.assertEqual(position1.y, 3)
        self.assertEqual(position1.x, 10)

    def test_setX(self):
        position1 = PacBotSimulation.Position(10, 3)
        position1.setX(22)
        self.assertEqual(position1.getX(), 22)
        self.assertEqual(position1.x, 22)
        self.assertEqual(position1.y, 3)


    def test_setY(self):
        position1 = PacBotSimulation.Position(10, 7)
        position1.setY(15)
        self.assertEqual(position1.getY(), 15)
        self.assertEqual(position1.y, 15)
        self.assertEqual(position1.x, 10)

    def test_equality(self):
        position1 = PacBotSimulation.Position(10, 7)
        position2 = PacBotSimulation.Position(3,5)
        position3 = PacBotSimulation.Position(10,7)

        self.assertNotEqual(position1, position2)
        self.assertEqual(position1, position3)
        self.assertNotEqual(position3, position2)


class TestConnectivityMask(unittest.TestCase):
    def __init__(self, *args, **argw):
        super(TestConnectivityMask, self).__init__(*args, **argw)

    def test_construction(self):
        connMask1 = PacBotSimulation.ConnectivityMask()
        self.assertEqual(connMask1.right, True)
        self.assertEqual(connMask1.left, True)
        self.assertEqual(connMask1.down, True)
        self.assertEqual(connMask1.up, True)
        self.assertEqual(connMask1.containFood, True)
        

    def test_removeFood(self):
        connMask1 = PacBotSimulation.ConnectivityMask()
        self.assertEqual(connMask1.containFood, True)
        connMask1.removeFood()
        self.assertEqual(connMask1.containFood, False)

    def test_equality(self):
        mask1 = PacBotSimulation.ConnectivityMask()
        mask2 = PacBotSimulation.ConnectivityMask()
        mask3 = PacBotSimulation.ConnectivityMask()

        mask1.setUp(False)
        mask2.setUp(False)

        self.assertEqual(mask1, mask2)
        self.assertNotEqual(mask3, mask2)
        self.assertNotEqual(mask1, mask3)


class TestArena(unittest.TestCase):
    def __init__(self, *args, **argw):
        super(TestArena, self).__init__(*args, **argw)

        self.ConnMask = PacBotSimulation.ConnectivityMask
        ConnMaskEqual = lambda test: isinstance(test, self.ConnMask)

        def maskConnectivity(testMaze):
            newMaze = []
            for item in testMaze:
                if(type(item) is list):
                    newMaze.append(maskConnectivity(item))
                else:
                    newMaze.append(ConnMaskEqual(item))
            return newMaze

        self.maskConnectivity = maskConnectivity


                    

    def test_construction(self):
        arena = PacBotSimulation.Arena(3,2)


        expectedResult = [ 
            [self.ConnMask(), self.ConnMask(), self.ConnMask()],
            [self.ConnMask(), self.ConnMask(), self.ConnMask()]
        ]

        expectedMask = self.maskConnectivity(expectedResult)
        actualMask = self.maskConnectivity(arena.maze)

        

        self.assertEqual(actualMask, expectedMask)

    def test_construction_maze_shape(self):
        arena = PacBotSimulation.Arena(10,3)

        col = len(arena.maze)
        row = len(arena.maze[0])
        self.assertEqual(col, 3)
        self.assertEqual(row, 10)

    def test_buildWallBetween_horizontal(self):
        x = 2
        y = 7

        arena = PacBotSimulation.Arena(10,10)

        row = arena.getRows() - y - 1
        col = x

        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x, y-1)

        row2 = arena.getRows() - (y-1) - 1

        self.assertEqual(arena.maze[col][row].canGoDown(), True)
        self.assertEqual(arena.maze[col][row2].canGoUp(), True)
        
        arena.buildWallBetween(pos1, pos2)

        self.assertEqual(arena.maze[col][row].canGoDown(), False)
        self.assertEqual(arena.maze[col][row2].canGoUp(), False)

        arena = PacBotSimulation.Arena(10, 10)


        self.assertEqual(arena.maze[col][row].canGoDown(), True)
        self.assertEqual(arena.maze[col][row2].canGoUp(), True)
        
        arena.buildWallBetween(pos2, pos1)

        self.assertEqual(arena.maze[col][row].canGoDown(), False)
        self.assertEqual(arena.maze[col][row2].canGoUp(), False)

    

    def test_buildWallBetween_verticle(self):
        x = 2
        y = 7

        arena = PacBotSimulation.Arena(10,10)

        row = arena.getRows() - y - 1
        col = x

        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x+1, y)

        col2 = x+1

        self.assertEqual(arena.maze[col][row].canGoRight(), True)
        self.assertEqual(arena.maze[col2][row].canGoLeft(), True)
        
        arena.buildWallBetween(pos1, pos2)

        self.assertEqual(arena.maze[col][row].canGoRight(), False)
        self.assertEqual(arena.maze[col2][row].canGoLeft(), False)

        arena = PacBotSimulation.Arena(10, 10)


        self.assertEqual(arena.maze[col][row].canGoRight(), True)
        self.assertEqual(arena.maze[col2][row].canGoLeft(), True)
        
        arena.buildWallBetween(pos2, pos1)

        self.assertEqual(arena.maze[col][row].canGoRight(), False)
        self.assertEqual(arena.maze[col2][row].canGoLeft(), False)
        
    def test_initalizeBoundryWall(self):
        arena = PacBotSimulation.Arena(3,4)

        raise Exception("test not implemented exception")

    def test_equality(self):
        arena1 = PacBotSimulation.Arena(5,2)
        arena2 = PacBotSimulation.Arena(3,4)
        arena3 = PacBotSimulation.Arena(5,2)
        arena4 = PacBotSimulation.Arena(5,2)

        arena4.maze[0][0].setUp(False)

        self.assertEqual(arena1==arena3, True)

        self.assertEqual(arena1, arena3)
        self.assertNotEqual(arena2, arena1)
        self.assertNotEqual(arena4, arena1)




def doTests(unit_test):
    suite = unittest.TestLoader().loadTestsFromTestCase(unit_test)
    unittest.TextTestRunner(verbosity=2).run(suite)

doTests(TestPosition)
doTests(TestConnectivityMask)
doTests(TestArena)
