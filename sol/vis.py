import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle, Circle


class Point():
    def __init__(self, x, y):
        self._x = x
        self._y = y
        return

    def __getitem__(self,i):
        return [self.x, self.y][i]

    def __str__(self):
        return '({},{})'.format(self.x,self.y)

    def __eq__(self, other):
        """2 Point are equal iff they are the same on the plane"""
        x_eq = self.x == other.x
        y_eq = self.y == other.y
        return x_eq and y_eq

    def __hash__(self):
        return hash(tuple(self))

    def copy(self):
        return Point(self.x, self.y)

    @property
    def x(self):
        """Return the x coordinate (vertical)"""
        return self._x

    @property
    def y(self):
        """Return the y coordinate (horizontal)"""
        return self._y
    
    def verticalMirror(self, mirror):
        """
            Returns a new Point which is result of mirroring
            this point throw a vertical mirror with X = mirror
        """
        mirror_y = self.y
        distToMir = self.x - mirror
        mirror_x = self.x - (2 * distToMir)
        return Point(mirror_x, mirror_y) 

    def horizontalMirror(self, mirror):
        """
            Returns a new Point which is result of mirroring
            this point throw a horizontal mirror with Y = mirror
        """
        mirror_x = self.x
        distToMir = self.y - mirror
        mirror_y = self.y - (2 * distToMir)
        return Point(mirror_x, mirror_y) 

    def distFromPoint(self, other):
        dx = (self.x - other.x)**2
        dy = (self.y - other.y)**2
        return math.sqrt(dx+dy)

    def isInlineOfFire(self, shooter, target):
        """
            shooter - Is a point from which a shot is fired.
            target - Is the point to which shooter is shooting.
            shooter and target define a segment in 2D space.
            Return True iff self is strictly (as adistinct point) 
            on that segment, I.E. blocking the shot. 
        """
        if self == shooter or self == target or target == shooter:
            raise Exception(
                'Must provide 3 distinct points to check line of fire'
            )

        tmpLeft = (shooter.y - self.y)*(target.x - self.x)
        tmpRight = (target.y - self.y)*(shooter.x - self.x)

        if tmpLeft == tmpRight:
            min_x = min(target.x, shooter.x)
            max_x = max(target.x, shooter.x)
            min_y = min(target.y, shooter.y)
            max_y = max(target.y, shooter.y)
            x_condition = min_x <= self.x <= max_x
            y_condition = min_y <= self.y <= max_y
            if x_condition and y_condition:
                return True
        return False

    def addPointToAx(self, ax, color):
        x,y = tuple(self)    
        ax.scatter(x, y, s=10, facecolor=color)
        return

    def addLineBetween2PointsToAx(self, ax, p):
        """add simple line plot to ax"""
        ax.plot((self.x, p.x), (self.y, p.y), 'k:',lw=1)
        return


class MyRectangle():
    def __init__(self, origPoint, dimensions):
        self.points = {
            'topRight': Point(
                origPoint[0] + dimensions[0],
                origPoint[1] + dimensions[1] 
            ),
            'topLeft': Point(
                origPoint[0],
                origPoint[1] + dimensions[1] 
            ),
            'bottomRight': Point(
                origPoint[0] + dimensions[0],
                origPoint[1] 
            ), 
            'bottomLeft': origPoint.copy()
        }
        self.length = dimensions[0]
        self.hight = dimensions[1]
        self.mirrors = {}
        return

    def __iter__(self):
        for i in self.points:
            yield i, self.points[i]
    
    def __str__(self):
        s = ''
        for n, p in self:
            s += '{}: {}\n'.format(n, str(p)) 
        return s[:-1] 

    @property
    def top(self):
        """The y componenet of the rectangl top side"""
        return self.points['topRight'].y

    @property
    def bottom(self):
        """The y componenet of the rectangl bottom side"""
        return self.points['bottomRight'].y

    @property
    def right(self):
        """The x componenet of the rectangl right side"""
        return self.points['topRight'].x

    @property
    def left(self):
        """The x componenet of the rectangl left side"""
        return self.points['topLeft'].x

    def isPointInside(self, p):
        """Return True iff point p is inside rec' border (including)"""
        x,y = p[0], p[1]
        A = self.left <= x <= self.right
        B = self.bottom <= y <= self.top
        return (A and B)
    
    def addRecToAx(self, ax, color='pink'):
        orignPoint = tuple(self.points['bottomLeft'])
        w = self.length
        h = self.hight
        ax.add_patch(Rectangle(
            orignPoint, w, h,
             edgecolor = color,
             fill=False,
             lw=1
        ))
        return

class Tile():
    """A 2 by 2 slice of R^2 with info about friend / foe"""
    def __init__(self, dimensions, origin, friend, foe):
        """
            dimensions - length times hight of tile. 
            origin - the bottome left x,y coordinates marking the beging.
            friens - line must not pass here befor hitting guard. 
            foe - x,y coordinates of target (guard).

            |----------|
            |-------G--|  ^ 
            |---F------|  | 
            |----------| <- length * hight tile
            ^ begins here
        """
        self.origin = Point(origin[0], origin[1])
        self.rec = MyRectangle(self.origin, dimensions)

        friend = Point(friend[0], friend[1])
        foe = Point(foe[0], foe[1])
        withinParam = self.rec.isPointInside(friend)
        withinParam &=  self.rec.isPointInside(foe)
        if not withinParam:  
            raise Exception('Point must be inside the rectangle') 
        
        self.friend = friend
        self.foe = foe
        self.dim = tuple(dimensions)
        self.mirrors = {}
        return
        
    def mirrorRight(self):
        mirrorXPosition = self.rec.right
        mirrorFriend = self.friend.verticalMirror(mirrorXPosition)
        mirrorFoe = self.foe.verticalMirror(mirrorXPosition)
        mirrorOrigin = self.rec.points['bottomRight']
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['right'] = newTile
        return newTile

    def mirrorUp(self):
        mirrorYPosition = self.rec.top
        mirrorFriend = self.friend.horizontalMirror(mirrorYPosition)
        mirrorFoe = self.foe.horizontalMirror(mirrorYPosition)
        mirrorOrigin = self.rec.points['topLeft']
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['up'] = newTile
        return newTile
    
    def mirrorDown(self):
        mirrorYPosition = self.rec.bottom
        mirrorFriend = self.friend.horizontalMirror(mirrorYPosition)
        mirrorFoe = self.foe.horizontalMirror(mirrorYPosition)
        mirrorOrigin = self.rec.points['topLeft']\
                            .horizontalMirror(mirrorYPosition)
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['down'] = newTile
        return newTile

    def mirrorLeft(self):
        mirrorXPosition = self.rec.left
        mirrorFriend = self.friend.verticalMirror(mirrorXPosition)
        mirrorFoe = self.foe.verticalMirror(mirrorXPosition)
        mirrorOrigin = self.rec.points['bottomRight']\
                            .verticalMirror(mirrorXPosition)
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['right'] = newTile
        return newTile

    def addTileToAx(self, ax, isOrign=False):
        friendColor = 'black' if isOrign else 'blue'
        recColor = 'black' if isOrign else 'pink'
        self.friend.addPointToAx(ax, friendColor)
        self.foe.addPointToAx(ax, 'red')
        self.rec.addRecToAx(ax,recColor)
        return


class Grid():
    def __init__(self, origTile, distance):
        self.originTile = origTile
        self.effectiveRange = distance
        origMe = origTile.friend
        
        self.matrix = grid = self.__gridInit__()
        
        # get all foes on the board
        targetList = [] 
        friendsList = []
        for l in grid:
            # print(f)
            targetList += map(lambda t: t.foe, l)
            friendsList += map(lambda t: t.friend, l)

        #remove duplicates 
        friendsList.remove(origMe)
        targetList = list(set(targetList))
        friendsList = list(set(friendsList))
        self.foes = tuple(targetList)
        self.friends = tuple(friendsList)
        
        #find ranges to target
        targetsInRange = map(
            lambda p: (p, origMe.distFromPoint(p)), 
            targetList
        )

        friendsInRange = map(
            lambda p: (p, origMe.distFromPoint(p)), 
            friendsList
        )

        #Remove out of range targets
        targetsInRange = filter(
            lambda t : t[1] <= distance,
            targetsInRange
        )
        
        friendsInRange = filter(
            lambda t : t[1] <= distance,
            friendsInRange
        )

        targetsInRange = sorted(targetsInRange, key = lambda t: t[1])
        friendsInRange = sorted(friendsInRange, key = lambda t: t[1])
        # for t in targetsInRange:
        #    print(t[0], t[1])
        
        self.targetsInRange = targetsInRange
        self.friendsInRange = friendsInRange

        clearShots = []
        # Run through possible targets in range
        for target in targetsInRange:
            #Check if there's something blocking the shot
            clearShot = True
            lst = targetsInRange+friendsInRange
            lst.remove(target)
            for p in lst:
                isInline = p[0].isInlineOfFire(origMe, target[0])
                if isInline:
                    clearShot = False
                    
            if clearShot:
                clearShots.append(target)

        self.clearShots = clearShots        
        return

    @property
    def numOfClearShots(self):
        return len(self.clearShots)

    def __gridInit__(self):
        origTile = self.originTile
        distance = self.effectiveRange
        dx, dy = origTile.dim
        x,y = tuple(origTile.friend)
        numOfTilesHorizon = int(math.ceil(float(distance+x)/dx))
        numOfTilesVert = int(math.ceil(float(distance+y)/dy))
        grid = [
            [None for _ in range(2*numOfTilesHorizon)] 
            for _ in range(numOfTilesVert) 
        ]
        origMe = origTile.friend
        grid[0][numOfTilesHorizon] = origTile

        for i in range(numOfTilesVert):
            if i>0 :
                grid[i][numOfTilesHorizon] = grid[i-1][numOfTilesHorizon].mirrorUp()
            grid[i][numOfTilesHorizon-1] = grid[i][numOfTilesHorizon].mirrorLeft()
            for j in range(1,numOfTilesHorizon):
                grid[i][numOfTilesHorizon+j] = grid[i][numOfTilesHorizon+j-1].mirrorRight()
                grid[i][numOfTilesHorizon-j-1] = grid[i][numOfTilesHorizon-j].mirrorLeft()
        
        lower = [
            [None for _ in range(2*numOfTilesHorizon)] 
            for _ in range(numOfTilesVert) 
        ]

        lower[0][numOfTilesHorizon] = grid[0][numOfTilesHorizon].mirrorDown()

        for i in range(numOfTilesVert):
            if i>0 :
                lower[i][numOfTilesHorizon] = lower[i-1][numOfTilesHorizon].mirrorDown()
            lower[i][numOfTilesHorizon-1] = lower[i][numOfTilesHorizon].mirrorLeft()
            for j in range(1,numOfTilesHorizon):
                lower[i][numOfTilesHorizon+j] = lower[i][numOfTilesHorizon+j-1].mirrorRight()
                lower[i][numOfTilesHorizon-j-1] = lower[i][numOfTilesHorizon-j].mirrorLeft()
        
        grid = grid+list(reversed(lower))
        return grid


    def drawGrid(self):
        #define Matplotlib figure and axis
        fig, ax = plt.subplots()
        grid = self.matrix
        origTile = self.originTile 
        origMe = self.originTile.friend
        r = self.effectiveRange

        # draw all tiles in the gride if they have a F/F point in effective range
        for l in grid:
            for t in l:
                a = t.friend.distFromPoint(origMe)
                b = t.foe.distFromPoint(origMe)
                #if a <= r or b <= r: 
                t.addTileToAx(ax)

        #mark the original Tile and shoot
        origTile.addTileToAx(ax, isOrign=True)
        
        # Draw circle in the radius of the shot's effective range
        ax.add_patch(Circle(
            tuple(origMe),
            r,
            edgecolor = 'green',
            fill=False,
            lw=1 
        ))
        
        # Draw clear shots:
        clearShots = self.clearShots
        for t in clearShots:
            origMe.addLineBetween2PointsToAx(ax, t[0])
        # origMe.addLineBetween2PointsToAx(ax, self.targetsInRange[-1][0])

        #display plot
        plt.show()
        return


#create simple line plot
# ax.plot([0, 10],[0, 10])

t = Tile([3, 2],[0,0],[1, 1],[2, 1])
g = Grid(t, 4)
print(g.numOfClearShots)
# g.drawGrid()

t1 = Tile([3,2], [0,0], [1,1], [2,1])
g1 = Grid(t1, 4)
print('{} = 7'.format(g.numOfClearShots))
# g1.drawGrid()

t2 = Tile([300,275], [0,0], [150,150], [185,100])
g2 = Grid(t2, 500)
print('{} = 9'.format(g.numOfClearShots))
g2.drawGrid()
# t1 = Tile([4, 4],[0,0],[1, 1],[2, 2])

# g1 = Grid(t1, 10)
# r = MyRectangle(Point(-1,-1), [2,4+2])
# r.addRecToAx(ax)
# p1 = Point(1,1)
# p0 = Point(0,0)
# p3 = Point(3,3)
# print(r.isPointInside(p0), r.isPointInside(p1), r.isPointInside(p3))
# t = Tile([3, 2],[0,0],[1, 1],[2, 1])
# t.addTileToAx(ax)

#add rectangle to plot
# ax.add_patch(Rectangle((1, 1), 2, 6,
#              edgecolor = 'pink',
#              facecolor = 'blue',
#              fill=False,
#              lw=1))

# p = Point(2,3)
# p0 = Point(0,0)
# p.addPointToAx(ax)
# p0.addPointToAx(ax)
#ax.scatter(1, 1, s=30, facecolor='black')
