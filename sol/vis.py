import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle


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

    def addPointToAx(self, ax, colur):
        x,y = tuple(self)    
        ax.scatter(x, y, s=10, facecolor=colur)
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
    
    def addRecToAx(self, ax):
        orignPoint = tuple(self.points['bottomLeft'])
        w = self.length
        h = self.hight
        ax.add_patch(Rectangle(
            orignPoint, w, h,
             edgecolor = 'pink',
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

    def mirrorUp(self, d='up'):
        mirrorYPosition = self.rec.top
        mirrorFriend = self.friend.horizontalMirror(mirrorYPosition)
        mirrorFoe = self.foe.horizontalMirror(mirrorYPosition)
        mirrorOrigin = self.rec.points['topLeft']
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['up'] = newTile
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

    def addTileToAx(self, ax):
        self.friend.addPointToAx(ax, 'blue')
        self.foe.addPointToAx(ax, 'red')
        self.rec.addRecToAx(ax)
        return


class Grid():
    def __init__(self, origTile, distance, ax):
        dx, dy = origTile.dim
        numOfTilesHorizon = int(math.ceil(float(distance)/dx))
        numOfTilesVert = int(math.ceil(float(distance)/dy))
        # print numOfTilesHorizon, numOfTilesVert
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
        
        for f in grid:
            print(f)
        self.matrix = grid
        # origTile.mirrorLeft()
        # get all foes on the board
        targetList = [] 
        for f in grid:
            # print(f)
            targetList += map(lambda t: t.foe, f)

        #remove duplicates 
        targetList = list(set(targetList))
        self.foes = tuple(targetList)

        #find ranges to target
        targetsInRange = map(
            lambda p: (p, origMe.distFromPoint(p)), 
            targetList
        )
        #Remove out of range targets
        targetsInRange = filter(
            lambda p,d: d <= distance,
            targetsInRange
        )
        #list(targetsInRange).sort(key = lambda t: t[1])
        # list(sorted(targetsInRange, key = lambda t: t[1]))
        #print(type(targetsInRange))
        #self.targetsInRange = list(sorted(targetsInRange, key = lambda t: t[1]))
        for l in grid:
            for t in l:
                t.addTileToAx(ax)
        return


#define Matplotlib figure and axis
fig, ax = plt.subplots()

#create simple line plot
# ax.plot([0, 10],[0, 10])

t = Tile([3, 2],[0,0],[1, 1],[2, 1])
g = Grid(t, 4, ax)
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

#display plot
plt.show()
