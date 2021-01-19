from math import ceil, sqrt

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
        """Return the euclidean R^2 distance"""
        dx = (self.x - other.x)**2
        dy = (self.y - other.y)**2
        return sqrt(dx+dy)

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

    def getSlope(self, other):
        """
            self and other - distinct point instances.
            Returns the slope of the R^2 line equation defined
            by the points self and other. I.E. if 'y = mx + b',
            is the line equation then getSlope returns m.
            If other point is directly above or bellow self,
            Return inf or -inf respectively.            
        """
        if self.x == other.x:
            if self.y < other.y:
                return float('inf') 
            return float('-inf') 
        return float(self.y - other.y)/float(self.x - other.x)


    def sgn(self, other):
        """
            self and other - distinct point instances.
            Returns 1 if the shot from travels in the positive 
            direction of the X axis, or, if self.x == other.x, 
            in the positive direction of th Y axis. -1 Otherwise.
        """
        s = 1
        if self.x == other.x: 
            if other.y < self.y:
                s = -1
        if other.x < self.x:
            s = -1
        return s


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
    
class Tile():
    """A width by height slice of R^2 with info about friend / foe"""
    def __init__(self, dimensions, origin, friend, foe):
        """
            dimensions - width times height of tile. 
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
        return
        
    def mirrorFactory(self, direction):
        mirrorConf = {
            'up': {
                'friend': self.friend.horizontalMirror(self.rec.top),
                'foe': self.foe.horizontalMirror(self.rec.top),
                'origin': self.rec.points['topLeft']
            },
            'down': {
                'friend': self.friend.horizontalMirror(self.rec.bottom),
                'foe': self.foe.horizontalMirror(self.rec.bottom),
                'origin': self.rec.points['topLeft']\
                            .horizontalMirror(self.rec.bottom)
            },
            'left': {
                'friend': self.friend.verticalMirror(self.rec.left),
                'foe': self.foe.verticalMirror(self.rec.left),
                'origin': self.rec.points['bottomRight']\
                            .verticalMirror(self.rec.left)
            },
            'right': {
                'friend': self.friend.verticalMirror(self.rec.right),
                'foe': self.foe.verticalMirror(self.rec.right),
                'origin': self.rec.points['bottomRight']
            }
        }

        try:
            direction = direction.lower()
            conf = mirrorConf[direction]
        except Exception as e:
            msg = str(e) + '\n'
            legalInput = mirrorConf.keys()
            msg += 'mirrorFactory only accepts {} as valid input!'\
                    .format(legalInput)
            raise Exception(msg)

        return Tile(
            self.dim, 
            conf['origin'], 
            conf['friend'], 
            conf['foe']
        )

class Grid():
    def __init__(self, origTile, distance):
        self.originTile = origTile
        self.effectiveRange = distance
        origMe = origTile.friend
        self.matrix = grid = self.__gridInit__()
        return

    @property
    def numOfClearShots(self):
        """
            Returns an integer of the number of distinct directions 
            that you can fire to hit the elite guard.
        """
        origMe = self.originTile.friend
        targetsInRange = self.acquireTargetsInRange()
        friendsInRange = self.identifyFriendlies()
        clearShots = self.getClearShots(origMe, targetsInRange, friendsInRange)
        return len(clearShots)

    def getClearShots(self, origMe, targetsInRange, friendsInRange):
        """
            Return a list of targets such that the shots are clear.
            I.E. there are no other friends or foes in the line of fire.
        """
        clearTargets = []
        shotsDict = {-1: {}, 1: {}}
        # Run through possible targets in range
        for target in targetsInRange:
            m = origMe.getSlope(target)
            sgn = origMe.sgn(target)
            rangeToTarget = origMe.distFromPoint(target)
            # Accurding to slope and direction of shot -
            # Conncat (target, range) couple to a list of targets 
            # in the same line of fire.
            if m in shotsDict[sgn].keys():
                shotsDict[sgn][m].append((target,rangeToTarget))
            else:
                shotsDict[sgn][m] = [(target,rangeToTarget)]

        for s in [-1,1]:
            for k in shotsDict[s]:
                # From all targets in the same line of fire - 
                # only store the closest one as shotsDict[s][k]
                # because one shot is one kill - shots stop where they hit.
                shotsDict[s][k] = sorted(shotsDict[s][k], key=lambda t: t[1])[0]

        # Iter through possible mirros of the shot's origin and check 
        # if they're in the way of the shot - avoiding friendly fire. 
        for p in friendsInRange:
            m = origMe.getSlope(p)
            sgn = origMe.sgn(p)
            # If line of fire exists
            if sgn in shotsDict:
                if m in shotsDict[sgn]:
                    # Make sure shot hits foe before freind
                    foe_r = shotsDict[sgn][m][1]
                    friend_r = origMe.distFromPoint(p)
                    # If you hit a friend before the foe - don't shot
                    if friend_r < foe_r:
                        del shotsDict[sgn][m]

        # Create a list of clear shots
        for s in [-1,1]:
            for k in shotsDict[s]:
                clearTargets.append(shotsDict[s][k])
        
        return clearTargets

    def acquireTargetsInRange(self):
        """Return a list of foes within effective range"""
        targetsInRange = []
        shootOrigin = self.originTile.friend
        d = self.effectiveRange
        for l in self.matrix:
            for t in l:
                if shootOrigin.distFromPoint(t.foe) <= d:
                    targetsInRange.append(t.foe)    
        return targetsInRange

    def identifyFriendlies(self):
        """
            Return a list of all friend points on the grid, 
            excluding the origin point.
        """
        frienlies = []
        shootOrigin = self.originTile.friend
        d = self.effectiveRange
        for l in self.matrix:
            for t in l:
                if shootOrigin.distFromPoint(t.friend) <= d:
                    if t.friend == shootOrigin:
                        continue
                    frienlies.append(t.friend)  
        return frienlies

    def __gridInit__(self):
        """
            Comupte the number of Tiles nedded and set them into a
            2D list. The list represents R^2 subset of rectangels in range 
            from the shot's origin in radius of the shot's effective range.
        """
        origTile = self.originTile
        distance = self.effectiveRange
        dx, dy = origTile.dim
        x,y = tuple(origTile.friend)
        # Clac num of tiles nedded for each axis
        numOfTilesHorizon = int(ceil(float(distance+x)/dx))
        numOfTilesVert = int(ceil(float(distance+y)/dy))
        # Generate positive and negative sides of Y axis
        upper = self.__gridHelper__(numOfTilesHorizon, numOfTilesVert, origTile)
        lower = self.__gridHelper__(
            numOfTilesHorizon, 
            numOfTilesVert, 
            origTile.mirrorFactory('down'),
            upsideDown=True
        ) 
        # Concat negative and positive sides of Y axis in the proper form
        grid = upper+list(reversed(lower))
        return grid

    def __gridHelper__(self, width, hieght, genTile, upsideDown=False):
        """
            Return a 2*width by hieght matrix such that each entry is
            a mirror of the generating tile (genTile) in its respective 
            direction. genTile is placed on (0,0) - grid[0][width] and
            is mirrored repeatedly in order to populate the grid.
            upsideDown takes into consideration the grid starts from 
            the top and runs down in the direction of Y's negative values.
        """
        vertMrrDirc = 'down' if upsideDown else 'up'
        grid = [
            [None for _ in range(2*width)] 
            for _ in range(hieght) 
        ]
        # Place original tile at the origins of the axies 
        grid[0][width] = genTile
        # Populate with mirrors
        for i in range(hieght):
            if i>0 :
                grid[i][width] = grid[i-1][width].mirrorFactory(vertMrrDirc)
            grid[i][width-1] = grid[i][width].mirrorFactory('left')
            for j in range(1,width):
                grid[i][width+j] = grid[i][width+j-1].mirrorFactory('right')
                grid[i][width-j-1] = grid[i][width-j].mirrorFactory('left')
        return grid
        

def solution(dimensions, your_position, guard_position, distance):
    """
        Observation: Let A and B be Points in R^2, 
        denote AB as the segment between points A and B. 
        Let O be a point in R^2 - the origin of a beam weapon shot. 
        Let M be a point on AB such that OM is the initial shot from 
        O in the direction of line AB. 
        As a beam weapon's shot bounces back in exactly the same direction it hits -
        let T be a point on the reflected beam. 
        Denote ang(OMA) as the angle between the lines OM and MA (as seen in the drawing). 
        Let OX be neutral extension of OM on the plane such that |OM| = |MX|.
        Then - by the terms of the problem, it holds that - ang(OMA) = ang(TMB).
        Also - ang(OMA) = ang(BMX) as the angles are alternating. 
        We get - ang(OMA) = ang(TMB) = ang(BMX). 
        If we consider AB as a mirror then simple geometry shows X is the mirror of T 
        and MX is the mirror of MT.

                       X
                      /|
                     / |
            A-------M--|-------B
                   / \ |
                  /   \|
                 O     T

        Thuse, if we want to know what happens after a beam is reflected off a wall, 
        it is sufficient to see what happens in the mirror. 

        Let a Tile be an 'width' by 'height' slice of R^2. 
        Let the "original-tile" be the tile defined by the room's measures in 
        the terms of the problem. The "original-tile" contains an origin point and a target.
        Let a "Mirrored Tile" be a tile we get as a result of mirroring an existing tile 
        through one of its sides. 
        For example: A mirroring of the left tile through its right side.
                |----------|        |----------|                   
                |-T----O---|  -->   |---O----T-|
                |----------|        |----------|

        Let a Grid be a subset of R^2 such that the "original-tile" is starting from (0,0). 
        The rest of the grid is made by mirroring the "original-tile" to all directions,
        as long as the tile is within the shot's effective range (AKA distance). 
        I.E. we are interested in tiles that have at least one of their points of interest 
        (a mirror of origin or target) within the circle originating at the shot's origin 
        (AKA your_position) with radius of the shot's effective range.
        Grid is essentially a list of tiles. As such, it induces a list of "foes" - 
        guard_position and its reflections within range, and a list of "friends" - 
        your_position and its reflections within range. 

        In order to solve the problem we must count the number of distinct lines that 
        start at the original-tile's shot's origin and connect to a target point before 
        passing through a friend or a foe (AKA - a clear shot). 
        For visual examples please see - 
        https://mega.nz/file/j2xySIII#3x2k4L8CROPCbq3RrBIZuMBO6VxXaUxaJ_HCxhyXHt0
        And -
        https://mega.nz/file/Gih2RQZT#dg6OqspFkFF1fvr7Ew-sy_zogCKLGUvo4Cn21jxJD30

        So - solution will create an original-tile, then, 
        with it a Grid, and, from the grid - return the number of clear shots.
    """
    orignTile = Tile(dimensions, [0,0], your_position, guard_position) 
    g = Grid(orignTile, distance)
    return g.numOfClearShots

if __name__ == "__main__":
    s = solution([3,2], [1,1], [2,1], 4)
    print('{} = 7'.format(s))

    s = solution([300,275], [150,150], [185,100], 500)
    print('{} = 9'.format(s))

    # print "start problem"
    s = solution([2,2+3], [1,2], [1,4], 11)
    print('{} = ?'.format(s))

    print "start problem"
    s = solution([3,3], [1,1], [2,2], 100)
    print('{} = ?'.format(s))

    # Point testing:
    # a = Point(0,0)
    # b = Point(1,1)
    # c = Point(0,1)

    # print a.getSlope(b)
    # print a.sgn(b)

    # print b.getSlope(a)
    # print b.sgn(a)

    # print a.getSlope(c)
    # print a.sgn(c)

    # print c.getSlope(a)
    # print c.sgn(a)
