import math
import json
from trianglesolver import solve, degree
from Components import Point, Triangle, Circle, Line
import copy
import test
import shapely
from shapely.geometry.point import Point as ShapelyPoint
from shapely.geometry.linestring import LineString


class GeometrySolver(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.problem_num = 1
        self.all_objects = {
            'edge': ['AB', 'BC', 'AC', 'AE', 'AG', 'AD', 'AH', 'AC', 'EG', 'EB', 'GB', 'DH', 'DC', 'HC', 'BC', 'BF',
                     'FC', 'r'],
            'angle': ['t1', 't2', 't3'],
            'vertex': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'O'],
            'area': ['a1', 'a2', 'a4', 'a5', 'a6', 'a3'],
            'arc': ['a1', 'a2', 'a4', 'a5', 'a6']}
        self.all_objects_general = {}

        self.solved_objects = {'edge': {}, 'angle': {}, 'vertex': {}, 'area': {}, 'arc': {}}
        self.solved_objects_genearal = {}
        self.triangle = None
        self.circle = None
        self.arc_map = {'a1':['E', 'G'], 'a2':['G', 'F'], 'a4': ['D', 'H'], 'a5':['F', 'H'], 'a6':['E','D'], 'a3':[]}
        self.lines = ['AB', 'BC']
        self.line_conn = {'A': ['B', 'C', 'D', 'E', 'G', 'H'],
                          'B': ['F', 'C'],
                          'C': [],
                          'E': ['G', 'B'], 'D': ['H', 'C'],
                          'G': ['B'], 'F': ['C'], 'H': ['C']}

        self.line_parent = {'E': 'A', 'G': 'A', 'D': 'A', 'H': 'A', 'F': 'B'}

    def printSolvedObjects(self):
        print("\n--Solved Term List--")
        for cg in self.solved_objects:
            print("\n" + cg + ":")
            for key in self.solved_objects[cg]:
                print(key + ":" + (
                            str(self.solved_objects[cg][key].x) + "," + str(self.solved_objects[cg][key].y)) if type(
                    self.solved_objects[cg][key]) == Point else key + ":" + str(self.solved_objects[cg][key]))

        if self.triangle:
            print("\nTriangle Data:")
            print("Edges:", "AB=", self.triangle.AB, "BC=", self.triangle.BC, "AC=", self.triangle.AC)
            print("Angles:", "t1=", self.triangle.t1, "t2=", self.triangle.t2, "t3=", self.triangle.t3)
            print("Area:", self.triangle.getArea())
            print("Heights(for each side as the base):", self.triangle.getHeights())
        if self.circle:
            print("\nCircle Data")
            self.circle.cal_parameter()
            print("Area:", self.circle.area)
            print("Perimeter:", self.circle.perimeter)
            if self.circle.center:
                print("Position", str(self.circle.center.x) + ',' + str(self.circle.center.y))
        return

    def get_solved_terms(self):
        res = "["
        added = set()
        for cg in self.solved_objects:
            for key in self.solved_objects[cg]:
                if cg + key in added:
                    continue
                if type(self.solved_objects[cg][key]) == Point:
                    value = '"(' + str(self.solved_objects[cg][key].x) + "," + str(
                        self.solved_objects[cg][key].y) + ')"'
                else:
                    value = str(self.solved_objects[cg][key])
                res += '{"type":"' + cg + '", "name":"' + key + '", "value":' + value + "},"
                added.add(cg + key)

        if self.triangle:

            var_map = {'t1': self.triangle.t1, 't2': self.triangle.t2, 't3': self.triangle.t3, 'AB': self.triangle.AB,
                       'AC': self.triangle.AC, 'BC': self.triangle.BC}
            for t in ['t1', 't2', 't3']:
                if "angle" + t in added:
                    continue
                res += '{"type":"angle", "name": "' + t + '", "value":' + str(var_map[t]) + '},'
            for t in ['AB', 'BC', 'AC']:
                if "edge" + t in added:
                    continue
                res += '{"type":"edge", "name": "' + t + '", "value":' + str(var_map[t]) + '},'

            res += '{"type":"area", "name": "ABC", "value":' + str(self.triangle.getArea()) + '},'

            heights = self.triangle.getHeights()
            for t in ['AB', 'BC', 'AC']:
                if "height" + t in added:
                    continue
                res += '{"type":"height", "name": "' + t + '", "value":' + str(heights[t]) + '},'

        if self.circle:
            if self.circle.perimeter:
                res += '{"type":"perimeter", "name": "O-perimeter", "value":' + str(self.circle.perimeter) + '},'
            if self.circle.area:
                res += '{"type":"area", "name": "O-area", "value":' + str(self.circle.perimeter) + '},'

        res = res[:-1]
        res += ']'
        return res

    # Functions that deal with and parse the inputs
    def problem_solver(self, objects):
        is_valid = self.parse_set_value(objects)
        if not is_valid:
            return None
        # if self.is_triangle_valid():
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

    def parse_set_value(self, objects, problem_num=1):
        '''
        Todo: Distribute the input objects into different corresponding functions
        :param objects:
        :return: if the object set is valid and set successfully
        '''
        # print(objects)
        self.problem_num = problem_num

        if problem_num == 2:
            self.line_conn = {'A': ['B', 'C'], 'B': ['C', 'E'], 'D': ['B', 'E'], }
            self.all_objects = {'vertex': ['A', 'B', 'C', 'D', 'E'],
                                'angle': ['t1', 't2', 't3', 't4', 't5'],
                                'edge': ['AB', 'AC', 'BC', 'DB', 'DE', 'BE'],
                                'area': [], 'arc': []}
        for item in objects:
            type = item['type']
            name = item['name']
            value = item['value']
            if name == 'O':
                value = value[1: -1]
                x, y = value.split(',')
                res = self.set_circle_position('O', float(x), float(y))
                if not res:
                    if self.debug:
                        print("Set Circle Position Failed")
                    return False
                self.circle_triangle_intersect()
            elif name == 'r':
                res = self.set_circle_radius(value)
                if not res:
                    if self.debug:
                        print("Set Circle Radius Failed")
                    return False
                self.circle_triangle_intersect()
            else:
                if type == 'edge':
                    name = self.map_line_name(name)
                if name not in self.all_objects[type]:
                    return False
                if type == "vertex":
                    value = value[1: -1]
                    x, y = value.split(',')
                    res = self.set_vertex(name, float(x), float(y))
                    if not res:
                        print("Vertex set failed")
                        return False
                elif type == "edge":
                    res = self.set_edge(name, int(value))
                    if not res:
                        if self.debug:
                            print("Edge set failed")
                        return False
                elif type == "angle":
                    if self.debug:
                        print("Setting Angle")
                    res = self.set_angle(name, int(value))
                    if not res:
                        if self.debug:
                            print("Angle set failed")
                        return False

                elif type == 'arc':
                    if self.debug:
                        print("Setting arc")
                    self.set_arc(name, value)

        self.cal_areas_arc()
        return True

    def get_triangle_angles(self):
        # def get_complement(angle):
        tar_angles = self.solved_objects['angle']
        if sum(t in tar_angles.keys() for t in ['t1', 't2', 't3']) == 2:
            if self.debug:
                print("Caluculating Complementing Angles")
            if 't1' in tar_angles.keys() and 't2' in tar_angles.keys():
                self.confirm_add('t3', 180 - (tar_angles['t1'] + tar_angles['t2']), 'angle')
            if 't1' in tar_angles.keys() and 't3' in tar_angles.keys():
                self.confirm_add('t2', 180 - (tar_angles['t1'] + tar_angles['t3']), 'angle')
            if 't3' in tar_angles.keys() and 't2' in tar_angles.keys():
                self.confirm_add('t1', 180 - (tar_angles['t2'] + tar_angles['t3']), 'angle')


    def get_complement_angles(self):
        # def get_complement(angle):
        tar_angles = self.solved_objects['angle']
        # print(tar_angles)
        if sum(t in tar_angles.keys() for t in ['t1', 't4', 't5']) == 2:
            if self.debug:
                print("Caluculating Complementing Angles")
            # print("Complement")
            if 't1' in tar_angles.keys() and 't4' in tar_angles.keys():
                self.confirm_add('t5', 180 - (tar_angles['t1'] + tar_angles['t4']), 'angle')
            if 't1' in tar_angles.keys() and 't5' in tar_angles.keys():
                self.confirm_add('t4', 180 - (tar_angles['t1'] + tar_angles['t5']), 'angle')
            if 't4' in tar_angles.keys() and 't5' in tar_angles.keys():
                self.confirm_add('t1', 180 - (tar_angles['t4'] + tar_angles['t5']), 'angle')

    # Functions that deal with the triangle ABC
    def identify_triangle(self):
        '''
        Check if current available terms are good to form a triangle
        :return:
        '''
        if 'AB' in self.solved_objects['edge'].keys() and 'BC' in self.solved_objects['edge'].keys() and 'AC' in \
                self.solved_objects['edge'].keys():
            if self.debug:
                print("Triangle formed from three sides!")
            self.triangle = Triangle({'edge': ['AB', 'AC', 'BC']}, self.solved_objects_genearal, "lll")
            # return

        if 'A' in self.solved_objects['vertex'].keys() and 'B' in self.solved_objects['vertex'].keys() and 'C' in \
                self.solved_objects['vertex'].keys():
            if self.debug:
                print("Triangle formed from three vertexes!")
            self.triangle = Triangle({'vertex': ['A', 'B', 'C']}, self.solved_objects_genearal, "vvv")
            # return

        # For side-angle-side condition
        if 'AB' in self.solved_objects['edge'] and 'BC' in self.solved_objects['edge']:
            if 't1' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AB', 'BC'], 'angle': ['t1']}, self.solved_objects_genearal, "lal")
            elif 't2' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AB', 'BC'], 'angle': ['t2']}, self.solved_objects_genearal, "lal")
            elif 't3' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AB', 'BC'], 'angle': ['t3']}, self.solved_objects_genearal, "lal")
        elif 'BC' in self.solved_objects['edge'] and 'AC' in self.solved_objects['edge']:
            if 't1' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AC', 'BC'], 'angle': ['t1']}, self.solved_objects_genearal, "lal")
            elif 't2' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AC', 'BC'], 'angle': ['t2']}, self.solved_objects_genearal, "lal")
            elif 't3' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AC', 'BC'], 'angle': ['t3']}, self.solved_objects_genearal, "lal")
        elif 'AB' in self.solved_objects['edge'] and 'AC' in self.solved_objects['edge']:
            if 't2' in self.solved_objects['angle']:
                self.triangle = Triangle({'edge': ['AB', 'AC'], 'angle': ['t2']}, self.solved_objects_genearal, "lal")


        # When two of the angles and one of the sides are known
        elif ('t1' in self.solved_objects['angle'] and 't2' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AC'], 'angle': ['t1', 't2']}, self.solved_objects_genearal, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['BC'], 'angle': ['t1', 't2']}, self.solved_objects_genearal, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AB'], 'angle': ['t1', 't2']}, self.solved_objects_genearal, "aal")

        elif ('t1' in self.solved_objects['angle'] and 't3' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AC'], 'angle': ['t1', 't3']}, self.solved_objects_genearal, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['BC'], 'angle': ['t1', 't2']}, self.solved_objects_genearal, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AB'], 'angle': ['t1', 't2']}, self.solved_objects_genearal, "aal")

        elif ('t2' in self.solved_objects['angle'] and 't3' in self.solved_objects['angle']):
            if 'AC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AC'], 'angle': ['t2', 't3']}, self.solved_objects_genearal, "aal")
            elif 'BC' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['BC'], 'angle': ['t2', 't3']}, self.solved_objects_genearal, "aal")
            elif 'AB' in self.solved_objects['edge']:
                self.triangle = Triangle({'edge': ['AB'], 'angle': ['t2', 't3']}, self.solved_objects_genearal, "aal")

    def is_triangle_valid(self):
        '''
        Check if the parameter for the triangle is valid
        :return: Boolean if it's valid
        '''
        if not self.triangle:
            self.identify_triangle()
            if self.triangle is not None:
                if self.debug:
                    print("Triangle formed! ", "Sides:", self.triangle.AB, self.triangle.BC, self.triangle.AC,
                          "Angles:", self.triangle.t1, self.triangle.t2, self.triangle.t3)
                self.circle_triangle_intersect()
                return True
            else:
                return False
        else:
            return False

    def checkTriangleValidByPoint(self, data, type):
        if type == 'lll':
            AB = data['AB']
            BC = data['BC']
            AC = data['AC']
            if AB >= (BC + AC) or BC >= (BC + AC) or AC >= (AB + BC):
                return False
        return True

    def triangle_detection(self):
        '''
        A function that keeps an eye on the conditions that are satisfied so far would be enough form the triangle
        :return:
        '''
        # print("Triangle Detection Triggered")
        if sum(x in ['t1', 't2', 't3'] for x in self.solved_objects['angle'].keys()) + sum(
                x in ['AB', 'BC', 'AC'] for x in self.solved_objects['edge'].keys()) >= 3:
            self.is_triangle_valid()
        return

    # Functions that set values for components
    def set_angle(self, name, value):
        '''
        :param name: string name of the angle
        :param value: int value in degree
        :return: Boolean if the value is valid and has been set successfully
        '''
        if self.debug:
            print(name, value)
        if value >= 360:
            return False
        if name == 't4' or name == 't5':
            if name not in self.solved_objects['angle'].keys():
                self.confirm_add(name, value, 'angle')
                return True
            else:
                return False
        other = []
        for i in range(1, 4):
            angle = 't' + str(i)
            if angle != name:
                other.append(angle)
        peer1, peer2 = other[0], other[1]
        if peer1 in self.solved_objects['angle'].keys() and peer2 in self.solved_objects['angle'].keys():
            if self.debug:
                print("Peer 1,2 exist")
            if (self.solved_objects['angle'][peer1] + self.solved_objects['angle'][peer2] + value) == 360:
                self.confirm_add(name, value, 'angle')
                return True
            else:
                return False
        elif peer1 in self.solved_objects['angle'].keys() and peer2 not in self.solved_objects['angle'].keys():
            if self.debug:
                print("Peer 1 exist ,2 not exist")
            if (self.solved_objects['angle'][peer1] + value) < 360:
                self.confirm_add(name, value, 'angle')
                return True
            else:
                return False
        elif peer1 not in self.solved_objects['angle'].keys() and peer2 in self.solved_objects['angle'].keys():
            if self.debug:
                print("Peer 1 not exit,2 exist")
            if (self.solved_objects['angle'][peer2] + value) < 360:
                self.confirm_add(name, value, 'angle')
                return True
            else:
                return False
        else:
            self.confirm_add(name, value, 'angle')
            return True

    def confirm_add(self, name, value, type):
        '''
        A function that write the value to the system's storage
        :param name:
        :param value:
        :param type:
        :return:
        '''
        self.solved_objects[type][name] = value
        self.solved_objects_genearal[name] = value
        if type == "angle" or type == "edge":
            self.triangle_detection()
        if type == "angle":
            if self.problem_num == 2:
                self.get_complement_angles()
            self.get_triangle_angles()

    def set_circle_radius(self, radius):
        if self.circle:
            if self.circle.radius:
                return False
            self.circle.radius = radius
            self.circle.cal_parameter()
        else:
            self.circle = Circle(radius=radius)
        return True

    def set_circle_position(self, name, x, y):
        if self.debug:
            print("Setting Circle")
        if self.circle:
            if self.circle.center is not None:
                return False
            self.circle.center = Point(x, y)
            self.circle.is_position_fixed = True
        else:
            self.circle = Circle(x=x, y=y)
        self.confirm_add('O', Point(x, y), "vertex")
        return True

    def set_vertex(self, name, x, y):
        if name == 'O':
            self.set_circle_position('O', x, y)

        def is_line_valid(p1, p2):
            '''
            If the new vertex is able to form a line, when that line already exists we should make sure they are the same, if it doesn't exist, we can set a new line's value
            :param p1:
            :param p2:
            :return:
            '''
            line_name = self.map_line_name(p1['name'] + p2['name'])
            point1, point2 = Point(p1['x'], p1['y']), Point(p2['x'], p2['y'])
            if self.debug:
                print(p1['x'], p1['y'], p2['x'], p2['y'])
            dist = self.distofTwoPoints(Point(p1['x'], p1['y']), Point(p2['x'], p2['y']))
            if line_name in self.solved_objects['edge'].keys():
                if self.debug:
                    print("Existing line and new line", line_name, self.solved_objects['edge'][line_name], dist)
                if dist != self.solved_objects['edge'][line_name]:
                    return False
                else:
                    return True
            else:
                if self.debug:
                    print("Line Name", line_name)
                if line_name in self.all_objects['edge']:
                    self.set_edge(self.map_line_name(line_name), dist, p1=point1, p2=point2)
                return True

        valid = True
        other = []
        for n in self.all_objects['vertex']:
            if n != name:
                other.append(n)
        for p in other:
            if p in self.solved_objects['vertex']:
                # print("Existing Vertexs:", p, name)
                obj2 = self.solved_objects['vertex'][p]
                a1 = {'name': name, 'x': x, 'y': y}
                a2 = {'name': p, 'x': self.solved_objects['vertex'][p].x, 'y': self.solved_objects['vertex'][p].y}
                if not is_line_valid(a1, a2):
                    valid = False

        if valid:
            self.solved_objects['vertex'][name] = Point(x, y)
            self.solved_objects_genearal[name] = Point(x, y)
            if self.debug:
                print("Succeed to set vertex", name)
            return True
        else:
            if self.debug:
                print("Failed to set vertex", name)
            return False

    def vertex_form_line(self, name, x, y):
        return

    # Functions that get values for components
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
            res = 360 - (
                        self.solved_objects['angle'][solved_angles[0]] + self.solved_objects['angle'][solved_angles[1]])
            self.solved_objects['angle'][name] = res
            return res
        else:
            return

    def get_edge(self, name):
        if name in self.solved_objects['edge']:
            return self.solved_objects['edge'][name]
        else:
            return None

    def get_vertex(self, name):
        if name in self.solved_objects['vertex']:
            return self.solved_objects['vertex'][name]
        return None

    def cal_areas_arc(self):
        if self.debug:
            print("Calculating Areas")
        # for vert in self.all_objects['vertex']:
        #     if vert not in self.solved_objects['vertex'] and vert != 'O':
        #         if self.debug:
        #             print(vert + " is not solved")
        #         return None
            # else:
            #     print(vert, self.solved_objects['vertex'][vert])
        # if not self.circle or not self.circle.center or not self.circle.radius:
        #     return None
        def check_arc_gettable(key):
            if key not in self.arc_map.keys():
                return False
            if not self.circle or not self.circle.center:
                return False
            for req in self.arc_map[key]:
                if req not in self.solved_objects['vertex'].keys():
                    return False
            return True

        for a_key in self.all_objects['area']:
            if not check_arc_gettable(a_key):
                continue
            area_val, arc_val = self.get_area_arc(a_key)
            if self.debug:
                print(area_val)
            if area_val:
                self.confirm_add(a_key, area_val, 'area')
            if arc_val:
                self.confirm_add(a_key, area_val, 'arc')

    def get_area_arc(self, name):
        def cal_sector(v1, v2, v1_name, v2_name):
            o_pos = self.solved_objects['vertex']['O']
            angle = self.angle_btw_points(v1, v2, o_pos)
            sector_area = (angle / 360) * self.circle.area
            # print("Area:", (v1.x, v1.y), (v2.x, v2.y))
            v1_O, v2_O, v1_v2 = math.sqrt((v1.x - o_pos.x) ** 2 + (v1.y - o_pos.y) ** 2), math.sqrt(
                (v2.x - o_pos.x) ** 2 + (v2.y - o_pos.y) ** 2), math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)
            v1_v2_name = self.map_line_name(v1_name + v2_name)
            # if not self.mostly_equal(v1_O, v2_O):
            #     print(name, "Not equal")
            #     return None, None
            temp_triangle = Triangle({'edge': ['AB', 'BC', 'AC']}, {'AB': v1_O, 'BC': v2_O, 'AC': v1_v2}, "lll")
            tri_area = temp_triangle.area
            tri_arc = (angle / 360) * self.circle.perimeter
            return (sector_area - tri_area), tri_arc

        def cal_circular(v1, v2, v3):
            o_pos = self.solved_objects['vertex']['O']
            v1_O, v2_O, v1_v2 = math.sqrt((v1.x - o_pos.x) ** 2 + (v1.y - o_pos.y) ** 2), math.sqrt(
                (v2.x - o_pos.x) ** 2 + (v2.y - o_pos.y) ** 2), math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)
            lower_triangle = Triangle({'edge': ['AB', 'BC', 'AC']}, {'AB': v2_O, 'BC': v1_O, 'AC': v1_v2}, "lll")
            v1_v3, v2_v3 = math.sqrt((v1.x - v3.x) ** 2 + (v1.y - v3.y) ** 2), math.sqrt(
                (v2.x - v3.x) ** 2 + (v2.y - v3.y) ** 2),
            # if not self.mostly_equal(v1_O, v2_O):
            #     return None, None
            upper_triangle = Triangle({'edge': ['AB', 'BC', 'AC']}, {'AB': v1_v3, 'BC': v2_v3, 'AC': v1_v2}, "lll")
            total_area = lower_triangle.area + upper_triangle.area
            angle = self.angle_btw_points(v1, v2, o_pos)
            sector_area = (angle / 360) * self.circle.area
            tri_arc = (angle / 360) * self.circle.perimeter
            return (total_area - sector_area), tri_arc

        if name == 'a1':
            area, arc = cal_sector(self.solved_objects['vertex']['E'], self.solved_objects['vertex']['G'], 'E', 'G')
            self.confirm_add(name, area, 'area')
            return area, arc
        elif name == 'a4':
            area, arc = cal_sector(self.solved_objects['vertex']['D'], self.solved_objects['vertex']['H'], 'D', 'H')
            self.confirm_add(name, area, 'area')
            return area, arc
        elif name == 'a2':
            area, arc = cal_circular(self.solved_objects['vertex']['G'], self.solved_objects['vertex']['F'],
                                     self.solved_objects['vertex']['B'])
            self.confirm_add(name, area, 'area')
            return area, arc
        elif name == 'a6':
            area, arc = cal_circular(self.solved_objects['vertex']['E'], self.solved_objects['vertex']['D'],
                                     self.solved_objects['vertex']['A'])
            self.confirm_add(name, area, 'area')
            return area, arc
        elif name == 'a5':
            area, arc = cal_circular(self.solved_objects['vertex']['F'], self.solved_objects['vertex']['H'],
                                     self.solved_objects['vertex']['C'])
            self.confirm_add(name, area, 'area')
            return area, arc
        elif name == 'a3':
            if 'a2' not in self.solved_objects['vertex'].keys():
                a2, _ = self.get_area_arc('a2')
            if 'a5' not in self.solved_objects['vertex'].keys():
                a5, _ = self.get_area_arc('a5')
            if 'a6' not in self.solved_objects['vertex'].keys():
                a6, _ = self.get_area_arc('a6')
            a2, a5, a6 = self.solved_objects['area']['a2'], self.solved_objects['area']['a5'], self.solved_objects['area']['a6']
            if not a2 or not a5 or not a6 or not self.triangle:
                return None, None
            return self.triangle.area - (a2 + a5 + a6), None

        return None, None

    def angle_btw_points(self, p0, p1, intersection):
        a = (intersection.x - p0.x) ** 2 + (intersection.y - p0.y) ** 2
        b = (intersection.x - p1.x) ** 2 + (intersection.y - p1.y) ** 2
        c = (p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2
        return math.acos((a + b - c) / math.sqrt(4 * a * b)) * 180 / math.pi

    def dot(self, vA, vB):
        return vA[0] * vB[0] + vA[1] * vB[1]

    # Return angle between two lines in degree
    def angle_btw_lines(self, lineA, lineB):
        # Get nicer vector form
        vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
        vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]
        dot_prod = self.dot(vA, vB)
        magA = self.dot(vA, vA) ** 0.5
        magB = self.dot(vB, vB) ** 0.5
        cos_ = dot_prod / magA / magB
        angle = math.acos(dot_prod / magB / magA)
        ang_deg = math.degrees(angle) % 360

        if ang_deg - 180 >= 0:
            # As in if statement
            return 360 - ang_deg
        else:

            return ang_deg

    def get_all_areas_arc(self):
        for key in self.all_objects['area']:
            self.get_area_arc(key)
        return

    def circle_triangle_intersect(self):
        if not self.circle or not self.circle.radius or not self.circle.center:
            return
        if not self.triangle or not self.triangle.position_fixed:
            return
        for line in ['AB', 'BC', 'AC']:
            if self.debug:
                print("Getting intersection of", line)
            if line == 'AB':
                E, G = self.get_intersection(line)
                if self.debug:
                    print("EG:", (E.x, E.y), (G.x, G.y))
                if not (self.set_vertex('E', E.x, E.y) and self.set_vertex('G', G.x, G.y)):
                    return False
            elif line == 'AC':
                D, H = self.get_intersection(line)
                if self.debug:
                    print("DH:", (D.x, D.y), (H.x, H.y))
                if not (self.set_vertex('D', D.x, D.y) and self.set_vertex('H', H.x, H.y)):
                    return False
            else:
                F = self.get_intersection(line)
                if self.debug:
                    print("F Point:", (F.x, F.y))
                if not self.set_vertex('F', F.x, F.y):
                    return False
        return True

    def get_intersection(self, line_name):
        p1, p2 = self.solved_objects['vertex'][line_name[0]], self.solved_objects['vertex'][line_name[1]]
        if self.debug:
            print("Intersecting:", self.circle.center.x, self.circle.center.y, self.circle.radius, "Line:",
                  (p1.x, p1.y), (p2.x, p2.y))
        circle = ShapelyPoint(self.circle.center.x, self.circle.center.y).buffer(self.circle.radius)
        line = LineString([(p1.x, p1.y), (p2.x, p2.y)])
        # print(line)
        intersections = circle.intersection(line).coords.xy
        if len(intersections[0]) == 2:
            p1, p2 = Point(intersections[0][0], intersections[1][0]), Point(intersections[0][1], intersections[1][1])
            if self.mostly_equal(p1, p2):
                return p2
            else:
                return p1, p2
        elif len(intersections[0]) == 1:
            return Point(intersections[0][0], intersections[1][0])

    def get_all(self):
        return self.solved_objects

    def set_edge(self, name, value, p1=None, p2=None):
        # print("Add Edge:", added_name, added_value, self.solved_objects['edge'])
        # if not self.solved_objects['edge'].keys() or name in ['AB', 'AC', 'BC']:
        #     self.add_edge(name, value)
        #     return True
        solved_objects = copy.deepcopy(self.solved_objects['edge'])
        if self.debug:
            print("New line name:", name, value)
        iter_num = 0
        for line in solved_objects.keys():
            iter_num += 1
            if line[1] == name[0] or name[1] == line[0]:
                comb_name_1 = self.map_line_name(line[0] + name[1])
                comb_name_2 = self.map_line_name(name[0] + line[1])
                if comb_name_1 in self.all_objects['edge']:
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    if comb_name_1 not in self.solved_objects['edge'].keys():
                        self.add_edge(name, value)
                        self.set_edge(comb_name_1, self.solved_objects['edge'][line] + value)
                    else:
                        if value >= self.solved_objects['edge'][comb_name_1]:
                            return False
                elif comb_name_2 in self.all_objects['edge']:
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    if comb_name_2 not in self.solved_objects['edge'].keys():
                        self.add_edge(name, value)
                        self.set_edge(comb_name_2, self.solved_objects['edge'][line] + value)
                    else:
                        if value >= self.solved_objects['edge'][comb_name_2]:
                            return False
                else:
                    self.add_edge(name, value)
            elif line[0] == name[0] or name[1] == line[1]:
                comb_name_3 = self.map_line_name(line[1] + name[1])
                comb_name_4 = self.map_line_name(line[0] + name[0])
                if comb_name_3 in self.all_objects['edge'] and comb_name_3 not in self.solved_objects['edge'].keys():
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    self.add_edge(name, value)
                    existed = self.solved_objects['edge'][line]
                    self.set_edge(comb_name_3, (existed - value) if existed > value else (value - existed))
                elif comb_name_4 in self.all_objects['edge'] and comb_name_4 not in self.solved_objects['edge'].keys():
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    self.add_edge(name, value)
                    existed = self.solved_objects['edge'][line]
                    self.set_edge(comb_name_3, (existed - value) if existed > value else (value - existed))
                else:
                    self.add_edge(name, value)
            else:
                comb_name_5 = line[1] + name[0]
                comb_name_6 = name[1] + line[0]
                # print(name, comb_name_5, comb_name_6)
                if comb_name_5 in self.all_objects['edge'] and comb_name_5 not in self.solved_objects['edge'].keys():
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    parent = line[0] + name[1]
                    if parent in solved_objects.keys():
                        parent_value = solved_objects[parent]
                    self.add_edge(name, value)
                    if parent_value:
                        existed = self.solved_objects['edge'][line]
                        self.set_edge(comb_name_5, parent_value - value - existed)
                elif comb_name_6 in self.all_objects['edge'] and comb_name_6 not in self.solved_objects['edge'].keys():
                    # print("Comb Name", name, line, comb_name_1, comb_name_2)
                    parent = name[0] + line[1]
                    if parent in solved_objects.keys():
                        parent_value = solved_objects[parent]
                    self.add_edge(name, value)
                    if parent_value:
                        existed = self.solved_objects['edge'][line]
                        self.set_edge(comb_name_6, parent_value - value - existed)
                self.add_edge(name, value)
        if not iter_num:
            self.add_edge(name, value)
        return True

    def set_arc(self, name, value):
        if name in self.solved_objects['arc'] or name not in self.all_objects['arc']:
            return False
        self.confirm_add(name, value, 'arc')
        self.check_circle_formation()

    def check_circle_formation(self):
        if sum(arc in self.solved_objects['arc'].keys() for arc in self.all_objects['arc']) == len(
                self.all_objects['arc']):
            perimeter = sum(self.solved_objects['arc'][arc] for arc in self.all_objects['arc'])
            radius = perimeter / (2 * math.pi)
            self.set_circle_radius(radius)

    def set_area(self, name, value):
        if name in self.solved_objects['area'] or name not in self.all_objects['area']:
            return False

    def add_edge(self, name, value, p1=None, p2=None):
        name = self.map_line_name(name)
        # print("Name", name)
        if name[1] not in self.line_conn[name[0]]:
            return False

        def justify_sides(a, b, c):
            if b in self.solved_objects['edge'] and c in self.solved_objects['edge']:
                b_v, c_v = self.solved_objects['edge'][b], self.solved_objects['edge'][c]
                if value >= (b_v + c_v) or b_v >= (value + c_v) or c_v >= (value + b_v): return False
            return True

        if name in ['AB', 'AC', 'BC']:
            if not justify_sides(name, 'BC', 'AC') or not justify_sides(name, 'AB', 'AC') or not justify_sides(name,
                                                                                                               'AB',
                                                                                                               'BC'):
                if self.debug:
                    print("Error: lengths of sides are not valid for a triangle!")
                return False
        # self.solved_objects['edge'][name] = Line(length=value, p1=p1, p2=p2)
        # self.solved_objects_genearal[name] = Line(length=value, p1=p1, p2=p2)
        self.confirm_add(name, value, "edge")
        self.triangle_detection()
        return True

    def mostly_equal(self, p1, p2):
        if isinstance(p1, float) and isinstance(p2, float):
            return abs(p1 - p2) < 10e-6
        if self.debug:
            print("Mostly Equal", p1.x, p1.y, p2.x, p2.y)
        if abs(p1.x - p2.x) < 10e-6 and abs(p1.y - p2.y) < 10e-6:
            return True
        else:
            return False

    # Functions for other things
    def map_line_name(self, name):
        # print(name)
        return name if name in self.all_objects['edge'] else name[1] + name[0]

    def distofTwoPoints(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


if __name__ == "__main__":
    # input_obj = input()
    # test = '[{"type":"vertex", "name":"A","value": "(0,0)"},{"type":"vertex", "name":"B", "value": "(3,3)"}, {"type":"vertex", "name":"C", "value": "(3,0)"},{"type":"vertex", "name":"r", "value":4}]'
    js_obj = json.loads(test.test9)
    print(js_obj[0]['value'])
    geo_solver = GeometrySolver(debug=True)
    geo_solver.parse_set_value(js_obj, problem_num=1)
    print(geo_solver.get_solved_terms())






