import math
import json
from collections import Counter
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
        self.length = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


class Triangle(object):

    def __init__(self, flags, data, type):
        print(flags, data, type)

    def form_triangle(self, type):
        return

    def calculateLine(self):
        self.BC = math.sqrt((self.B.x - self.C.x) ** 2 + (self.B.y - self.C.y) ** 2)
        self.AC = math.sqrt((self.A.x - self.C.x) ** 2 + (self.A.y - self.C.y) ** 2)
        self.AB = math.sqrt((self.A.x - self.B.x) ** 2 + (self.A.y - self.B.y) ** 2)

    def getArea(self):
        '''
        Todo: Calculating the area based on length of each side
        :return:
        '''
        s = (self.BC + self.AC + self.AB) / 2
        self.area = math.sqrt(s * (s - self.BC) * (s - self.AC) * (s - self.AB))
        return self.area

    def getHeights(self):
        '''
        Todo: Get the heights of this triangle with different bases
        :return: a dictionary mapping from each side as the base to the corresponding height
        '''
        if not self.area:
            return None
        else:
            return {'AB':self.area/self.AB, 'BC': self.area/self.BC, 'AC': self.area/self.AC }


class Circle(object):
    def __init__(self, center, radius):
        self.center, self.radius = center, radius
        self.area = (radius**2) * math.pi
        self.perimeter = (radius*2) * math.pi

class Obj(object):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class GeometrySolver(object):
    def __init__(self):
        self.all_objects = {'edge':['AB', 'BC', 'AC', 'AE', 'EG', 'BG', 'BF', 'CF', 'CH', 'DH', 'AD'],
                            'angle':['t1', 't2', 't3'],
                            'vertex': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                            'area': ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']}
        self.label_pts_map = {}
        self.label_line_map = {}
        self.solved_objects = {'edge':{}, 'angle':{}, 'vertex':{}, 'area':{}}
        for char in "ABCDEFGH":
            self.all_objects[char] = Obj(char, 4, None)

        for i in range(1, 4):
            angle = 't' + str(i)
            self.all_objects[angle] = Obj(angle, 1, None)

        for i in range(1, 7):
            area = 'a' + str(i)
            self.all_objects[area] = Obj(area, 2, None)
        self.lines = ['AB', 'BC']
        self.line_conn = {'A':['B','C','D','E','G','H'],
						'B':['A', 'E', 'G', 'F', 'C'],
						'C':['F', 'B', 'H', 'D', 'A'],
                          'E':['G'], 'D': ['H']}

    def problem_solver(self, objects):
        is_valid = self.parse_set_value(objects)
        if not is_valid:
            return None
        res = {}
        for key in self.all_objects.keys():
            res[key] = {}
            for obj in self.all_objects[key]:
                if key == 'edge':
                    res[key][obj] = self.get_edge(obj)
                elif key == 'vertex':
                    res[key][obj] = self.get_vertex(obj)
                elif key == 'angle':
                    res[key][obj] = self.get_angle(obj)
        return res

    # def test(self, objects):
    #     for item in objects.items:
    def identify_triangle(self):
        triangle = None
        # For side-angle-side condition
        if 'AB' in self.solved_objects['edge'] and 'BC' in self.solved_objects['edge'] and 't1' in self.solved_objects['angle']:
            self.triangle = Triangle(['AB', 't1', 'BC'], self.solved_objects, "lal")
        elif 'BC' in self.solved_objects['edge'] and 'AC' in self.solved_objects['edge'] and 't3' in self.solved_objects['angle']:
            self.triangle = Triangle(['BC', 't3', 'AC'], self.solved_objects, "lal")
        elif 'AB' in self.solved_objects['edge'] and 'AC' in self.solved_objects['edge'] and 't2' in self.solved_objects['angle']:
            self.triangle = Triangle(['AB', 't2', 'AC'], self.solved_objects, "lal")
        #For angle-side-angle condition
        elif 't1' in self.solved_objects['angle'] and 't2' in self.solved_objects['angle'] and 'AB' in self.solved_objects['edge']:
            self.triangle = Triangle(['t1', 'AB', 't2'], self.solved_objects, "ala")
        elif 't1' in self.solved_objects['angle'] and 't3' in self.solved_objects['angle'] and 'BC' in self.solved_objects['edge']:
            self.triangle = Triangle(['t1', 'BC', 't3'], self.solved_objects, "ala")
        elif 't3' in self.solved_objects['angle'] and 't2' in self.solved_objects['angle'] and 'AC' in self.solved_objects['edge']:
            self.triangle = Triangle(['t2', 'AC', 't3'], self.solved_objects, "ala")

        #When two of the angles and one of the sides are known
        elif ('t1' in self.solved_objects['angle'] and 't2' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't2', 'AC'], self.solved_objects, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't2', 'BC'], self.solved_objects, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't2', 'AB'], self.solved_objects, "aal")

        elif ('t1' in self.solved_objects['angle'] and 't3' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't3', 'AC'], self.solved_objects, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't3', 'BC'], self.solved_objects, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle(['t1', 't3', 'AB'], self.solved_objects, "aal")

        elif ('t2' in self.solved_objects['angle'] and 't3' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t2', 't3', 'AC'], self.solved_objects, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle(['t2', 't3', 'BC'], self.solved_objects, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle(['t2', 't3', 'AB'], self.solved_objects, "aal")


    def parse_set_value(self, objects):
        '''
        Todo: Distribute the input objects into different corresponding functions
        :param objects:
        :return: if the object set is valid and set successfully
        '''
        print(objects)
        for item in objects:
            type = item['type']
            name = item['name']
            value = item['value']
            if name not in self.all_objects[type]:
                return False
            if type == "vertex":
                value = value[1: -1]
                x, y = value.split(',')
                res = self.set_vertex(name, x, y)
                if not res:
                    return False
            elif type == "edge":
                res = self.set_edge(name, int(value))
                if not res:
                    return False
            elif type == "angle":
                print("Setting Angle")
                res = self.set_angle(name, int(value))
                if not res:
                    return False
        return True

    def set_angle(self, name, value):
        '''
        :param name: string name of the angle
        :param value: int value in degree
        :return: Boolean if the value is valid and has been set successfully
        '''
        print(name, value)
        if value >= 360:
            return False
        other = []
        for i in range(1, 4):
            angle = 't' + str(i)
            if angle != name:
                other.append(angle)
        peer1, peer2 = other[0], other[1]
        if peer1 in self.solved_objects['angle'].keys() and peer2 in self.solved_objects['angle'].keys():
            print("Peer 1,2 exist")
            if (self.solved_objects['angle'][peer1] + self.solved_objects['angle'][peer2] + value) == 360:
                self.solved_objects['angle'][name] = value
                return True
            else:
                return False
        elif peer1 in self.solved_objects['angle'].keys() and peer2 not in self.solved_objects['angle'].keys():
            print("Peer 1 exist ,2 not exist")
            if (self.solved_objects['angle'][peer1] + value) < 360:
                self.solved_objects['angle'][name] = value
                return True
            else:
                return False
        elif peer1 not in self.solved_objects['angle'].keys() and peer2 in self.solved_objects['angle'].keys():
            print("Peer 1 not exit,2 exist")
            if (self.solved_objects['angle'][peer2] + value) < 360:
                self.solved_objects['angle'][name] = value
                return True
            else:
                return False
        else:
            self.solved_objects['angle'][name] = value
            return True

    def set_edge(self, name , value):
        if name[1] not in self.line_conn[name[0]]:
            return False
        self.solved_objects['edge'][name] = value
        return True

    def set_vertex(self, name, x, y):
        self.solved_objects['vertex'][name] = Point(x, y)
        return True

    def get_angle(self, name):
        if name in self.solved_objects.keys():
            return self.solved_objects[name]
        return self.get_unsolved_angle(name)

    def get_unsolved_angle(self, name):
        angles = ['t1', 't2', 't3']
        solved_angles = []
        for t in angles:
            if t in self.solved_objects['angle'].keys():
                solved_angles.append(t)

        if len(solved_angles) == 2:
            res = 360 - (self.solved_objects['angle'][solved_angles[0]] + self.solved_objects['angle'][solved_angles[1]])
            self.solved_objects['angle'][name] = res
            return res
        else:
            return

    def form_triangle(self):
        return

    def get_edge(self, name):
        return

    def get_vertex(self, name):
        return

    def get_all(self):
        return

    def checkTriangleValidByPoint(self, point_a, point_b, point_c):
        line_a = math.sqrt((point_b.y - point_c.y) ** 2 + (point_b.x - point_c.x) ** 2)
        line_b = math.sqrt((point_a.y - point_c.y) ** 2 + (point_a.x - point_c.x) ** 2)
        line_c = math.sqrt((point_a.y - point_b.y) ** 2 + (point_a.x - point_b.x) ** 2)
        if not line_a or not line_b or not line_c:
            return False
        if line_a >= line_b + line_c or line_b >= line_c + line_a or line_c >= line_a + line_b:
            return False
        return True


    def addPoints(self, x, y, label):
        # Add a point to the graph
        self.label_pts_map[label] = Point(x, y)
        print("Point " + label + " Added")
        return label

    def getPointPos(self, label):
        # Get the position of a point
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
    # input_obj = input()
    test = '[{"type":"edge", "name":"AB","value": 4}, {"type":"angle", "name":"t1","value": 50}, {"type":"angle", "name":"t2","value": 40}]'
    js_obj = json.loads(test)
    print(js_obj[0]['value'])
    geo_solver = GeometrySolver()
    geo_solver.parse_set_value(js_obj)
    print(geo_solver.solved_objects)
    geo_solver.identify_triangle()





