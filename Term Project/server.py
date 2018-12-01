#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import cgitb; cgitb.enable()
import json
from GeometrySolver import GeometrySolver

if __name__ == '__main__':

    data = cgi.FieldStorage()
    print "Content-Type: text/html\n"
    size = data['size'].value
    problem = int(data['problem'].value)
    input_data = '['
    # print(size,data['data[0][type]'].value)
    for i in range(int(size)):
        type_of_input = data['data['+ str(i) +'][type]'].value
        # print(type_of_input)
        if type_of_input == 'vertex':
            input_data += '{ "type":"' + type_of_input + '", "name":"' + data['data['+ str(i) +'][name]'].value + '", "value":"' + data['data['+ str(i) +'][value]'].value + '"},'
        else:
            input_data += '{ "type":"' + type_of_input + '", "name":"' + data['data['+ str(i) +'][name]'].value + '", "value":' + data['data['+ str(i) +'][value]'].value + '},'

    input_data = input_data[:-1]
    input_data += ']'
    # print("input",input_data)
    geo_solver = GeometrySolver()
    js_obj = json.loads(input_data)
    # print(js_obj)
    geo_solver.parse_set_value(js_obj, problem_num = problem)
    print(geo_solver.get_solved_terms())