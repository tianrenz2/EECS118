#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()


class GeometryLayout(object):
	def __init__(self):
		self.geo_solver = None
		#self.all_objects = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6']
		self.topology = {'A':['B','C','D','E','G','H'], 
						'B':['A', 'E', 'G', 'F', 'C'], 
						'C':['F', 'B', 'H', 'D', 'A']}
		self.angles = ['BAC', 'CAB', 'EAD', 'DAE', 'GAD', 'DAG']

	def initView(self):
		print "Content-type: text/html\n\n";
		print "<html>"
		print "<script src='http://code.jquery.com/jquery-2.0.3.js'></script>"
		print "<h1>Problem 1</h1>"
		print "<img src='http://localhost:8080/problem1.png' width='400'>"

		print """
				<h4>Variable names:</h4>
				<p>Lines: AB, BC, AC, AE, AG, AD, AH, AC, EG, EB, GB, DH, DC, HC, BC, BF, FC, r</p>
				<p>Vertex: A, B, C, D, E, F, G, H, O</p>
				<p>Arc: a1, a2, a4, a5, a6</p>
				<p>Angles: t1, t2, t3</p>
				<p>Area: a1, a2, a3, a4, a5, a6</p>
			"""
		print '<h2>Set Values for Components in the Graph:</h2>'
#		print '<form action="problem1.py" method="get">'
		print """<input id="choice1" name="inputType" type="radio" value="angle"><label for="choice1">Angle</label>
				 <input id="choice2" name="inputType" type="radio" value="area"><label for="choice2">Area</label>
				 <input id="choice3" name="inputType" type="radio" value="edge"><label for="choice3">Line Segment</label>
		  		 <input id="choice4" name="inputType" type="radio" value="vertex"><label for="choice4">Vertex</label>
		  		 <input id="choice5" name="inputType" type="radio" value="arc"><label for="choice5">Arc</label>
		  		 </br></br>""" 

		print 'Name: <input type="text" id="compName"> Value:<input type="text" id="compValue">'
		print '<input type="hidden" name="pagetype" value="1">'
		print '<button onclick= "setVal()"> Add </button>'
		print '<button onclick= "submit()"> Submit </button>'
#		print '</form>'
		print '<p>Note: if you set value for a vertex, please follow the format of (x,y)</p>'
		print '<p>Please choose the correct check box for your input type.</p>'
		print """<h4>Suggested inputs:</h4>
				<p>1. A: (0,0), B: (3,1), C: (3,0), r: 1, O: (2,0.5) </p>
				<p>2. AB: 4, t1: 40, BC: 3, O: (3,3) </p>
				<p>3. a1: 1, a2: 3, a4: 2, a5: 2, a6: 4 </p>
				"""


		print '<h3>Value Set:</h3>'
		print '<div id="input_container"></div>'

		print '<h3>Result Set:</h3>'
		print '<div id="output_container"></div>'

		print '<h2>Get Values for Components in the Graph:</h2>'
		# print '<form id="getform" action="problem1.py" method="get">'
		print 'Name: <input type="text" id="getCompName">'
		print """<input id="choice1" name="inputType" type="radio" value="angle"><label for="choice1">Angle</label>
				 <input id="choice2" name="inputType" type="radio" value="area"><label for="choice2">Area</label>
				 <input id="choice3" name="inputType" type="radio" value="line"><label for="choice3">Line Segment</label>
		  		 <input id="choice4" name="inputType" type="radio" value="point"><label for="choice4">Point</label>
		  		 <input id="choice5" name="inputType" type="radio" value="arc"><label for="choice5">Arc</label>
		  		 </br></br>""" 
		print '<input type="hidden" name="pagetype" value="2">'
		print '<button onclick= "getVal()"> Get </button>'
		# print '</form>'
		
		print """
			<script type="text/javascript">
				var req_data = {'data':[], 'size': 0, 'problem':1}
				var rec_data = null
				function setVal() {
					var selValue = $('input[name=inputType]:checked').val() 

					var setName = $('#compName').val()
					var setVal = $('#compValue').val()

					if (setName != null){
						console.log(selValue, setName, setVal)

						var container = $('#input_container')
						container.append('<p>'+setName + ': ' + setVal + '</p>')
						req_data['data'].push({'type':selValue, 'name':setName, 'value': setVal})
						req_data['size'] += 1
						console.log(container)
					}



				}

				function submit() {
					str_req_data = JSON.stringify(req_data)
					console.log(str_req_data)
					$.ajax({
				            url: "http://localhost:8080/cgitest/cgi-bin/server.py",
				            type: "POST",
				            data: req_data,
				            success: function(response){
				                    $("#div").html(response);
				                }
				    }).done( function(data){
				    	console.log("Data got")
				    	console.log(data)
				    	var response=jQuery.parseJSON(data);
				    	console.log(jQuery.type(response))
				    	if (jQuery.type(response) == "array" && response.length > 0){
				    		rec_data = response
				    		displayAll()
				    	}else{
				    		$('#output_container').append("<p>Sorry, Invalid Inputs...</p>")
				    	}
				    });

				}


				function getVal() {
					var selValue = $('input[name=inputType]:checked').val(); 
					

					var getName = $('#getCompName').val()
					var type = $('input[name=inputType]:checked').val() 
					console.log(getName, type)
					if(rec_data.length > 0){
						for (var i = 0; i < rec_data.length; i ++){
							if(rec_data[i]['name'] == getName && type == rec_data[i]['type']){
								$('#get_container').append("<p>"+ type + ", " +rec_data[i]['name'] + ":" + rec_data[i]['value'] +"</p>")
							}
						}
					}
					
					
				}

				function displayAll(){
					console.log("Displaying")
					for(var i = 0; i < rec_data.length; i++){
						var val = ""
						if(rec_data[i]['type'] == 'height'){
							val = "Triangle Height"
							$('#output_container').append("<p><h4>" + val + "</h4>" + rec_data[i]['name'] + ", " + rec_data[i]['value'] + "</p>" )

						}else{
							$('#output_container').append("<p>" + rec_data[i]['type'] + ": " + rec_data[i]['name'] + ", " + rec_data[i]['value'] + "</p>" )
						}
						
					}
				}

			</script>
			  """

		print '</html>'

		form = cgi.FieldStorage()
		pagetype = form.getvalue('pagetype')

		if pagetype:
			if pagetype == '1':
				var_type = form.getvalue('inputType')
				pagetype = form.getvalue('pagetype')
				set_name = form.getvalue('compName')
				set_val = form.getvalue('compValue')
				self.setValues(set_name, set_val, var_type)					
			elif pagetype == '2':
				get_name = form.getvalue('compName')
				print "Trying to get the value for",get_name
#Type: angle-0, area-1, line-2, point-3
	def setValues(self, name, value, typename):
		type_map = {'angle': 0, 'area': 1, 'line': 2, 'point': 3}
		type = type_map[typename]
		print name
		if type == 0:
			if name not in self.angles:
				print "<h3>This element does not exist in the graph!</h3>"
		return


if __name__ == "__main__":
	geo_layout = GeometryLayout()
	geo_layout.initView()

