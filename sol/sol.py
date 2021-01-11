import math

def printRoom(dimensions, your_position, guard_position):
    room = list(reversed(
        [[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])]
    ))
    room[your_position[1]][your_position[0]] = 1
    room[guard_position[1]][guard_position[0]] = 2
    for l in room:
        print l

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = math.sqrt(x*x + y*y) 
        self.theta = math.atan(float(self.y)/self.x) if x != 0 else math.pi/2

    def __getitem__(self,i):
        return [self.x, self.y][i]

    def __str__(self):
        return '({},{})'.format(self.x,self.y)

    def __eq__(self, other):
        x_eq = self.x == other.x
        y_eq = self.y == other.y
        return x_eq and y_eq

    def copy(self):
        return Point(self.x, self.y)

    @property
    def x(self):
        """Return the x coordinate (vertical)"""
        return self.x

    @property
    def y(self):
        """Return the y coordinate (horizontal)"""
        return self.y
    
    @property
    def polarCoordinates(self):
        return self.r, self.theta

    @property 
    def moveByPoint(self):
        """
            returns a function f.
            f: R^2 -> R^2 f "moves" the plane by how much 
            it would take to move the point "self" to (0,0). 
            f(x,y) = (x-self.x, y-self.y)
        """
        return lambda x,y: x-self.x, y-self.y

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

    @classmethod
    def pointFromPolar(cls, r, theta):
        x = r * math.sin(theta)
        y = r * math.cos(theta)
        return cls(x,y)

p = Point(2,3)
p0 = Point(0,0)
o0 = Point(0,0)
print p == p0
print p0 == o0
# print p.verticalMirror(3)
# print p.horizontalMirror(2)

class LineEquation():
    def __init__(self, s, b):
        # of the form y = sx + b
        self.slope = s
        self.b = b
        self.y = lambda x: s*x + b
        self.r = lambda theta: b / (math.sin(theta) - s*math.cos(theta))

    def __call__(self, x, polar = False):
        return self.r(x) if polar else self.y(x)
    
    def __str__(self):        
        return 'y = {}*x + {}'.format(self.slope,self.b)

    def __eq__(self, other):
        slopesEq = self.slope == other.slope
        bEq = self.b == other.b 
        return slopesEq and bEq 

    @property
    def polar(self):
        m, b = self.slope, self.b
        return '{} / (math.sin(theta) - {}*math.cos(theta))'.format(b,m)

    def isPointOnLine(self, point): 
        return point[1] == self.y(point[0])

    @classmethod
    def lineBetween2Points(cls,p1,p2):
        # y - y1 = m(x - x1)
        # b = y1 - m*x1
        slope = float(p2[1]-p1[1]) / float(p2[0]-p1[0])
        b =  p1[1] - (slope * p1[0]) 
        return cls(slope, b)

    @classmethod
    def lineFromslopeAndPoint(cls,p,m):
        # y - y1 = m(x - x1)
        # b = y1 - m*x1
        b =  p1[1] - (m * p1[0]) 
        return cls(m, b)

# l1 = LineEquation(1,0)
# print l1
# p1 = Point(0,0)
# p2 = Point(1,1)
# l2 = LineEquation.lineBetween2Points(p1,p2)
# print l2
# print l1 == l2 
# print l1.isPointOnLine(Point(2,2))
# print l2.isPointOnLine(Point(2,2))
# l3 = LineEquation.lineBetween2Points(Point(3,7),Point(5,11))
# print l3
# l4 = LineEquation.lineBetween2Points(Point(2,3),Point(6,-5)) 
# print l4
# l7 = LineEquation.lineBetween2Points(Point(-3,4),Point(5, -2))
# print l7
# print l3.polar
# l4.polar
# l7.polar

class Rectangle():
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


    def mirrorFactory(self, direction):
        """
            Return a Rectangle instance with same dimensions.
            starting form the end of this rectangle, and is the mirror 
            of this one. 
            Keep a pointer for ref.
        """
        directions = {
            'east': 'bottomRight',
            'west': 'bottomLeft',
            'north': 'topLeft',
            'south': None
        }

        d = direction.lower()
        if d not in directions:
            msg = 'Mirror only takes {} as valid directions.\n'\
                .format(directions.keys())
            msg += 'Cannot mirror in direction {}!!!'\
                .format(d)
            raise Exception(msg)

        new_dim = (self.length, self.hight)
        if d == 'south':
            new_x = self.points['bottomLeft'][0]
            new_y = self.points['bottomLeft'][0] - self.hight
            new_orig = Point(new_x, new_y)
        else:
            new_orig = self.points[directions[d]]
        
        new_rec = Rectangle(new_orig, new_dim)
        self.mirrors[d] = new_rec
        return new_rec
        

# r = Rectangle(Point(0,0), [2,2])
# p1 = Point(1,1)
# p0 = Point(0,0)
# p3 = Point(3,3)
# print r.isPointInside(p0), r.isPointInside(p1), r.isPointInside(p3)
#print r.mirrorRight()
# print 'east: ', r.mirrorFactory('east')
# print '\nwest: ' , r.mirrorFactory('west')
# print '\nnorth', r.mirrorFactory('north')
# print '\nsouth', r.mirrorFactory('south')

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
        self.rec = Rectangle(self.origin, dimensions)

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
        
    def mirrorFactory(self, d='right'):
        directions = {'left': None, 'right': None, 'up': None}
        
        mirrorXPosition = self.rec.right
        mirrorFriend = self.friend.verticalMirror(mirrorXPosition)
        mirrorFoe = self.foe.verticalMirror(mirrorXPosition)
        # print "{} -> {}, {} -> {} by mirror x = {}".\
        #     format(
        #         self.friend, 
        #         mirrorFriend, 
        #         self.foe,
        #         mirrorFoe,
        #         mirrorXPosition
        #     )
        mirrorOrigin = self.rec.points['bottomRight']
        d = self.dim

        newTile = Tile(d, mirrorOrigin, mirrorFriend, mirrorFoe)
        self.mirrors['right'] = newTile
        return newTile

t = Tile([3, 2],[0,0],[1, 1],[2, 1])
# tErr = Tile([3, 2],[0,0],[1, 9],[2, 1])
print t.mirrorFactory('right').friend

def solution(dimensions, your_position, guard_position, distance):
    x1, y1 = your_position
    x2, y2 = guard_position
    return [x2-x1, y2-y1]

#print solution([3, 2],[1, 1],[2, 1],4)
#printRoom([3, 2],[1, 1],[2, 1])