

<!-- Note -->
<!-- Please make sure the following jar files are in your tomcat/lib/ directory,
commons-io-2.6.jar, commons-fileupload-1.3.3.jar, servlet-api.jar,
otherwise it is going to shoot an error -->

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
	<link href="hw1/style.css" rel="stylesheet">
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>EECS 118 File Uploading</title>


</head>

<body>
	<h1>Galleries</h1>
	<%



	String sql_sel_gal = "select * from gallery";
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

	if(request != null && request.getParameter("Change")!=null){

		request.getParameter("artist");
		String name = request.getParameter("Name");
		String by = request.getParameter("Birthyear");
		String country = request.getParameter("Country");
		String des = request.getParameter("Description");

		String sql_insert_art = "insert into artist values(default, ?, ?, ?, ?)";

		PreparedStatement artpstmt = con.prepareStatement(sql_insert_art,Statement.RETURN_GENERATED_KEYS);
          artpstmt.clearParameters();
          artpstmt.setString(1, name);
          artpstmt.setString(2, by);
          artpstmt.setString(3, country);
          artpstmt.setString(4, des);
          artpstmt.executeUpdate();
          ResultSet art_rs=artpstmt.getGeneratedKeys();
          while (art_rs.next()) {
            out.println("Successfully added this artist. Customer_ID:"+art_rs.getInt(1));
          }


	}else{

	    if(!con.isClosed()){
			PreparedStatement ps=(PreparedStatement)con.prepareStatement(sql_sel_gal);
			ResultSet rs=ps.executeQuery();
			while(rs.next()){
				String gallery_id = rs.getString("gallery_id");
				String name=rs.getString("name");
				String description=rs.getString("description");

				out.println("<a href='http://localhost:8080/hw1/gallery.jsp?gallery_id="+ gallery_id +"&gName="+name + "&existed=1" +"'><div class='galleryContainer'> <h3>" + name + "</h3>" + description +"</div></a>");
				out.println("</br>");

			}

			out.println("<div id='modifyWindow' class='modal'><div class='modal-content'> <span class='modspan'>&times;</span> <form method='post'> <h4>Artist Name:</h4> <input type='text' name='Name'> <h4>Birth Year:</h4> <input type='text' name='Birthyear'> <h4>Country:</h4> <input type='text' name='Conntry'> <h4>Description:</h4> <input type='text' name='Description'> <input type='hidden' name='Change' value='1'> <br /> <br /> <input type='submit' value='Create' /> </form> </div> </div>");

			out.println("<div id='findWindow' class='modal'><div class='modal-content'> <span class='findspan'>&times;</span> <form action='hw1/search.jsp' method='post'> <input type='radio' name='condition' value='type' />Type<br> <input type='radio' name='condition' value='yearrange'/> Year Range(ex:1988-1999) <br> <input type='radio' name='condition' value='artistname'/> Artist Name <br>  <input type='text' name='keyword'><input type='hidden' name='search' value='image'> <input type='submit' value='Search' /> </form> </div> </div>");


			out.println("<div id='findArtistWindow' class='modal'><div class='modal-content'> <span class='findartistspan'>&times;</span> <form action='hw1/search.jsp' method='post'> <input type='radio' name='condition' value='country' />Country<br> <input type='radio' name='condition' value='birthyear'/> Birth Year <br>  <input type='text' name='keyword'><input type='hidden' name='search' value='artist'> <input type='submit' value='Search' /> </form> </div> </div>");
	    }else{
	      out.println("Database Not Connected!");
	    }


}

%>


	<button id="myBtn" name="create">Create Gallery</button>
	<button id='modify' name='create'>Create Artist</button>
	<button id='find' name='create'>Find Image</button>
	<button id='findArtist' name='create'>Find Artist</button>

	<!-- The Modal -->
	<div id="myModal" class="modal">
	  <!-- Modal content -->
	  <div class="modal-content">
	    <span class="close">&times;</span>
	    <form action="hw1/gallery.jsp" method="post">
			<h4>Gallery Name:</h4>
			<input type="text" name="gName">
			<h4>Description:</h4>
			<input type="text" name="Description">
			<br />
			<br />
			<input type="submit" value="Create" />
		</form>

	  </div>


<script>
var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
btn.onclick = function() {
    modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

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


  var findWindow = document.getElementById('findWindow');
  var findbtn = document.getElementById("find");
  var findspan = document.getElementsByClassName("findspan")[0];
  findbtn.onclick = function() {
      findWindow.style.display = "block";
  }
  // When the user clicks on <span> (x), close the modal
  findspan.onclick = function() {
      findWindow.style.display = "none";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          findWindow.style.display = "none";
      }
  }


  var findArtistWindow = document.getElementById('findArtistWindow');
  var findArtistbtn = document.getElementById("findArtist");
  var findartistspan = document.getElementsByClassName("findartistspan")[0];
  findArtistbtn.onclick = function() {
      findArtistWindow.style.display = "block";
  }
  // When the user clicks on <span> (x), close the modal
  findartistspan.onclick = function() {
      findArtistWindow.style.display = "none";
  }
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          findArtistWindow.style.display = "none";
      }
  }



</script>

</body>


</html>
