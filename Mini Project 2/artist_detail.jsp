<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*, javax.servlet.*" %>
<%@ page import="javax.servlet.http.*" %>
<%@ page import="org.apache.commons.fileupload.*" %>
<%@ page import="org.apache.commons.fileupload.disk.*" %>
<%@ page import="org.apache.commons.fileupload.servlet.*" %>
<%@ page import="org.apache.commons.io.output.*" %>
<%@ page import="java.sql.*"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<link href="style.css" rel="stylesheet">
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>EECS 118 File Uploading</title>


</head>

<body>
	<%

	if(request != null){
		String artist_id = request.getParameter("artist_id");
		String sel_artist = "select * from artist where artist_id="+artist_id;
		try {
	      Class.forName("com.mysql.jdbc.Driver").newInstance();
	    }
	    catch(Exception e) {
	      out.println("can't load mysql driver");
	      out.println(e.toString());
	    }
	    String dbUrl="jdbc:mysql://127.0.0.1:3306/gallery?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
	    String id="gallery";
	    String pwd="eecs118";
	    Connection con = DriverManager.getConnection(dbUrl,id,pwd);

	    if(!con.isClosed()){
			PreparedStatement ps=(PreparedStatement)con.prepareStatement(sel_artist);
			ResultSet rs=ps.executeQuery();
			while(rs.next()){
				String name=rs.getString("name");
				int birthyear = rs.getInt("birth_year");
				String description=rs.getString("description");
				String country = rs.getString("country");

				out.println("<table><tr> <td>Name: </td> <td>"+ name +"</td> </tr> <tr> <td>Birthyear: </td> <td>"+ birthyear +"</td> </tr> <tr> <td>Country: </td> <td>"+ country +"</td> </tr> <td>Description: </td> <td>"+ description +"</td> </tr></table>");
			}

			out.println("<div id='modifyWindow' class='modal'><div class='modal-content'> <span class='modspan'>&times;</span> <form action='modify.jsp' method='post'> <h4>Artist Name:</h4> <input type='text' name='Name'> <h4>Birth Year:</h4> <input type='text' name='Birthyear'> <h4>Country:</h4> <input type='text' name='Conntry'> <h4>Description:</h4> <input type='text' name='Description'> <input type='hidden' name='from' value='artist_detail'> <input type='hidden' name='artist_id' value='"+ artist_id +"'> <br /> <br /> <input type='submit' value='Create' /> </form> </div> </div>");
	    }else{
	      out.println("Database Not Connected!");
	    }
	}

%>
	<button id='modify' name='create'>Modify</button>

<script type="text/javascript">
	
  var modWindow = document.getElementById('modifyWindow');
  var modbtn = document.getElementById("modify");
  var modspan = document.getElementsByClassName("modspan")[0];
  modbtn.onclick = function() {
      modWindow.style.display = "block";
  }
  // When the user clicks on <span> (x), close the modal
  modspan.onclick = function() {
      modWindow.style.display = "none";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modWindow.style.display = "none";
      }
  }
</script>


</body>


</html>
