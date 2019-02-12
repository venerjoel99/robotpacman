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

    def test_getWallCount(self):
        mask1 = PacBotSimulation.ConnectivityMask()
        self.assertEqual(mask1.getWallCount(), 0)

        mask1.setUp(False)
        self.assertEqual(mask1.getWallCount(), 1)

        mask1.setLeft(False)
        self.assertEqual(mask1.getWallCount(), 2)

        mask1.setDown(False)
        self.assertEqual(mask1.getWallCount(), 3)

        mask1.setRight(False)
        self.assertEqual(mask1.getWallCount(), 4)


class TestArena(unittest.TestCase):
    def __init__(self, *args, **argw):
        super(TestArena, self).__init__(*args, **argw)

        self.ConnMask = PacBotSimulation.ConnectivityMask

    def test_construction(self):
        arena = PacBotSimulation.Arena(3,2)


        expectedResult = [ 
            [self.ConnMask(), self.ConnMask(), self.ConnMask()],
            [self.ConnMask(), self.ConnMask(), self.ConnMask()]
        ]

        self.assertEqual(arena.maze, expectedResult)
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
        
        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x, y-1)

        self.assertEqual(arena.getMask(x,y  ,"xy").canGoDown(), True)
        self.assertEqual(arena.getMask(x,y-1,"xy").canGoUp(), True)

        arena.buildWallBetween(pos1, pos2)

        self.assertEqual(arena.getMask(x,y  ,"xy").canGoDown(), False)
        self.assertEqual(arena.getMask(x,y-1,"xy").canGoUp(), False)

    def test_buildWallBetween_horizontal_order_independent(self):
        x = 2
        y = 7

        arena = PacBotSimulation.Arena(10,10)
        
        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x, y-1)

        self.assertEqual(arena.getMask(x,y  ,"xy").canGoDown(), True)
        self.assertEqual(arena.getMask(x,y-1,"xy").canGoUp(), True)

        arena.buildWallBetween(pos2, pos1)

        self.assertEqual(arena.getMask(x,y  ,"xy").canGoDown(), False)
        self.assertEqual(arena.getMask(x,y-1,"xy").canGoUp(), False)

    def test_buildWallBetween_verticle(self):
        x = 2
        y = 7

        arena = PacBotSimulation.Arena(10,10)

        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x+1, y)

        self.assertEqual(arena.getMask(x  ,y,"xy").canGoRight(), True)
        self.assertEqual(arena.getMask(x+1,y,"xy").canGoLeft(), True)
        
        arena.buildWallBetween(pos1, pos2)

        self.assertEqual(arena.getMask(x  ,y,"xy").canGoRight(), False)
        self.assertEqual(arena.getMask(x+1,y,"xy").canGoLeft(), False)

    def test_buildWallBetween_verticle_order_independent(self):
        x = 2
        y = 7

        arena = PacBotSimulation.Arena(10,10)

        pos1 = PacBotSimulation.Position(x,y)
        pos2 = PacBotSimulation.Position(x+1, y)

        self.assertEqual(arena.getMask(x  ,y,"xy").canGoRight(), True)
        self.assertEqual(arena.getMask(x+1,y,"xy").canGoLeft(), True)
        
        arena.buildWallBetween(pos2, pos1)

        self.assertEqual(arena.getMask(x  ,y,"xy").canGoRight(), False)
        self.assertEqual(arena.getMask(x+1,y,"xy").canGoLeft(), False)
    
    
    def test_initalizeBoundryWall(self):
        arena = PacBotSimulation.Arena(3,4)
        arena.initalizeBoundryWall()

        noUp = self.ConnMask()
        noUp.setUp(False)

        noDown = self.ConnMask()
        noDown.setDown(False)

        noLeft = self.ConnMask()
        noLeft.setLeft(False)

        noRight = self.ConnMask()
        noRight.setRight(False)

        topLeft = self.ConnMask()
        topLeft.setLeft(False)
        topLeft.setUp(False)

        topRight = self.ConnMask()
        topRight.setRight(False)
        topRight.setUp(False)

        bottomLeft = self.ConnMask()
        bottomLeft.setLeft(False)
        bottomLeft.setDown(False)

        bottomRight = self.ConnMask()
        bottomRight.setRight(False)
        bottomRight.setDown(False)

        middle = self.ConnMask()

        expected = [
            [  topLeft, noLeft, noLeft, bottomLeft],
            [  noUp,    middle,  middle, noDown],
            [ topRight, noRight, noRight, bottomRight]
        ]

        self.assertTrue(arena.maze, expected)


    def test_getMask(self):
        arena = PacBotSimulation.Arena(5,5)
        mask1 = self.ConnMask()
        mask1.setUp(False)

        arena.maze[2][3].setUp(False)

        self.assertEqual(arena.getMask(2,3)      , mask1)
        self.assertEqual(arena.getMask(2,1, "xy"), mask1)

    def test_setMask(self):
        arena = PacBotSimulation.Arena(5,5)

        mask1 = self.ConnMask()
        mask1.setUp(False)

        arena.setMask(2,3, mask1)
        self.assertEqual(arena.getMask(2,3), mask1)

        arena.setMask(2,2, mask1, "xy")
        self.assertEqual(arena.getMask(2,2, "xy"), mask1)




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
