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
	if(request.getParameter("img_id") != null){
		String img_id = request.getParameter("img_id");
	    String dbUrl="jdbc:mysql://127.0.0.1:3306/gallery?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
	    String id="gallery";
	    String pwd="eecs118";
	    Connection con = DriverManager.getConnection(dbUrl,id,pwd);

		if(request.getParameter("delete") != null){
			String del_img = "delete from image where image_id=" + img_id;
			String del_dt = "delete from detail where image_id=" + img_id;
			PreparedStatement ps_del_img=(PreparedStatement)con.prepareStatement(del_img);
		    ps_del_img.executeUpdate();
			
			PreparedStatement ps_del_dt=(PreparedStatement)con.prepareStatement(del_dt);
		    ps_del_dt.executeUpdate();



		    out.println("The image has been deleted...");

		}else{

			try {
		      Class.forName("com.mysql.jdbc.Driver").newInstance();
		    }
		    catch(Exception e) {
		      out.println("can't load mysql driver");
		      out.println(e.toString());
		    }


		    String select_detail = "select * from detail where image_id=" + img_id;
		    String select_img = "select * from image where image_id=" + img_id;


		  

			PreparedStatement ps_img=(PreparedStatement)con.prepareStatement(select_img);
		    ResultSet rs_img=ps_img.executeQuery();
		    int artist_id = -1;
		    while(rs_img.next()){
		    	String title = rs_img.getString("title");
		    	String link = rs_img.getString("link");
		    	artist_id = rs_img.getInt("artist_id");
		    	out.println("<h2>" + title + "</h2>");
		    	out.println("<img src='" + link + "'>");
			}

			String sel_artist = "select name from artist where artist_id="+artist_id;

			PreparedStatement ps_art=(PreparedStatement)con.prepareStatement(sel_artist);
		    ResultSet rs_art=ps_art.executeQuery();
		    String artist_name = "";
		    while(rs_art.next()){
		    	artist_name = rs_art.getString("name");
			}


		    PreparedStatement ps_dt=(PreparedStatement)con.prepareStatement(select_detail);
		    ResultSet rs_dt=ps_dt.executeQuery();



		    while(rs_dt.next()){
				String year = rs_dt.getString("year");
				String type=rs_dt.getString("type");
				String width=rs_dt.getString("width");
				String height=rs_dt.getString("height");
				String location=rs_dt.getString("location");
				String description=rs_dt.getString("description");
				String artist_url = "http://localhost:8080/hw1/artist_detail.jsp?artist_id="+artist_id;  

				out.println("<table><tr> <td>Year: </td> <td>"+ year +"</td> </tr> <tr> <td>Type: </td> <td>"+ type +"</td> </tr> <td>Width: </td> <td>"+ width +"</td> </tr> <td>Height: </td> <td>"+ height +"</td> </tr> <td>Location: </td> <td>"+ location +"</td> </tr> <td>Description: </td> <td>"+ description +"</td> </tr> <td>Artist Name: </td> <td><a href='"+ artist_url + "'>"+ artist_name +"</td> </tr> </table>");

			}
  				out.println("<div id='modifyWindow' class='modal'><div class='modal-content'> <span class='modspan'>&times;</span> <form action='modify.jsp' method='post'> <h4>Title:</h4> <input type='text' name='Title'> <h4>Link:</h4> <input type='text' name='link'> <h4>Year:</h4> <input type='text' name='Year'><h4>Type:</h4> <input type='text' name='Type'> <h4>Width:</h4> <input type='text' name='Width'> <h4>Height:</h4> <input type='text' name='Height'><h4>Location:</h4> <input type='text' name='Location'> <h4>Description:</h4> <input type='text' name='Description'> <input type='hidden' name='from' value='img_detail'> <input type='hidden' name='img_id' value='"+ img_id +"'> <br /> <br /> <input type='submit' value='Modify' /> </form> </div> </div>");

			String delete_url = "http://localhost:8080/hw1/image_detail.jsp?img_id=" + img_id + "&delete=1";
			out.println("<div></div>");
			out.println("<div><a href='"+ delete_url +"'>Delete This Image</a></div>");
		}

	}
%>
	<button id='modify' name='create'>Modify</button>


<script>

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
      if (event.target == modWindow) {
          modWindow.style.display = "none";
      }
  }


  
</script>

</body>


</html>