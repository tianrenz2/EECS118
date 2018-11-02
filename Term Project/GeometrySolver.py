import math

'''
Read Me:
This file has yet implemented making points, making lines, calculating angles functions. It can be directly run and tested. 
'''

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class GeometrySolver(object):
    def __init__(self):
        self.label_pts_map = {}
        self.label_line_map = {}

    def addPoints(self, x, y, label):
        self.label_pts_map[label] = Point(x, y)
        print("Point " + label + " Added")
        return label

    def getPointPos(self, label):
        if label in self.label_pts_map.keys():
            return self.label_pts_map[label]
        else:
            return None

    def printPoints(self):
        print("-- Current Points --")
        for key in self.label_pts_map.keys():
            print(key + ": (" + str(self.label_pts_map[key].x) + ',' + str(self.label_pts_map[key].y) + ')')

    def getPtsDist(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def connectPoints(self, label1, label2):
        if label1 not in self.label_pts_map.keys() or label2 not in self.label_pts_map.keys():
            return None
        newlabel = label1 + '-' + label2
        self.label_line_map[newlabel] = Line(self.label_pts_map[label1], self.label_pts_map[label2])
        return newlabel

    def getLineLength(self, label):
        if label in self.label_line_map.keys():
            p1 = self.label_line_map[label].p1
            p2 = self.label_line_map[label].p2
            return self.getPtsDist(p1, p2)
        else:
            return None

    #Return angle made by three points in degree
    def angle_btw_points(self, p0, p1, intersection):
        a = (intersection[0]-p0[0])**2 + (intersection[1]-p0[1])**2
        b = (intersection[0]-p1[0])**2 + (intersection[1]-p1[1])**2
        c = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
        return math.acos((a+b-c)/math.sqrt(4*a*b))* 180/math.pi

    def dot(self, vA, vB):
        return vA[0]*vB[0]+vA[1]*vB[1]

#Return angle between two lines in degree
    def angle_btw_lines(self, lineA, lineB):
        # Get nicer vector form
        vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
        vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
        dot_prod = self.dot(vA, vB)
        magA = self.dot(vA, vA)**0.5
        magB = self.dot(vB, vB)**0.5
        cos_ = dot_prod/magA/magB
        angle = math.acos(dot_prod/magB/magA)
        ang_deg = math.degrees(angle)%360

        if ang_deg-180>=0:
            # As in if statement
            return 360 - ang_deg
        else:

            return ang_deg



if __name__ == "__main__":
    geo_solver = GeometrySolver()

    print("Try Basic Operations:")
# Add points
    geo_solver.addPoints(1, 2, 'A')
    geo_solver.addPoints(5, 4, 'B')

# Get Point List
    geo_solver.printPoints()

# Connect two points
    geo_solver.connectPoints('A', 'B')

    print("Length of A-B",geo_solver.getLineLength('A-B'))

    print("\n-- Test Angle Functions --")
# Define two lines
    line1 = ((0, 0), (5, 5))
    line2 = ((0, 0), (5, 0))

# Define three points
    p1 = (1, 1)
    p2 = (5, 4)
    intersection = (0, 0)


# Get the angle between the line1 and line2
    print("Calculating the angle between", line1, "and", line2)
    print("The Angle's Value:",geo_solver.angle_btw_lines(line1, line2))
    print('\n')
# Get the angle made of p1, p2 and intersection
    print("Calculating the angle of", p1, p2, "and", intersection, "where the intersection is", intersection)
    print(geo_solver.angle_btw_points(p1, p2, intersection))