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

	   	String dbUrl="jdbc:mysql://127.0.0.1:3306/gallery?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";

	    String id="gallery";
	    String pwd="eecs118";
	      try {
	        Class.forName("com.mysql.jdbc.Driver").newInstance();
	    }
	        catch(Exception e) {
	        out.println("can't load mysql driver");
	        out.println(e.toString());
	      }

	    Connection con = DriverManager.getConnection(dbUrl,id,pwd);

	    String search_type = request.getParameter("search");
		String final_sql = "";
		String mid_sql = "";
		String condition = request.getParameter("condition");
		String keyword = request.getParameter("keyword");



		PreparedStatement mid_ps = null;
		PreparedStatement final_ps = null;
		ResultSet mid_rs = null;
		ResultSet final_rs = null;
		if(search_type.equals("image")){


			if (condition.equals("type")){
				mid_sql = "select * from image where image_id=(select image_id from detail where type='" + keyword + "')";
				

			}else if(condition.equals("yearrange")){
				String[] a = keyword.split("-");
				int lower = Integer.parseInt(a[0]);
				int upper = Integer.parseInt(a[1]);

				mid_sql = "select * from image where image_id=(select image_id from detail where year>" + lower + " and year<" + upper + ")";

			}else if(condition.equals("artistname")){
				mid_sql = "select * from image where artist_id=(select artist_id from artist where name='"+ keyword +"')";
			}

			mid_ps=(PreparedStatement)con.prepareStatement(mid_sql);
			mid_rs=mid_ps.executeQuery();
	        while(mid_rs.next()){
	          String img_id=mid_rs.getString("image_id");
	          String img_title=mid_rs.getString("title");

	          String link = mid_rs.getString("link");

	          String img_link = "http://localhost:8080/hw1/image_detail.jsp?img_id=" + img_id;
	          out.println("<div class='responsive'><div class='gallery'><a target='_blank' href='" + img_link +"'><img src='"+ link +"' alt='Mountains' width='600' height='400'></a><div class='desc'>"+ img_title +"</div></div></div>");
	        }
	    }else if(search_type.equals("artist")){
	    	if(condition.equals("birthyear")){
	    		mid_sql = "select name, artist_id from artist where birth_year="+Integer.parseInt(keyword);

	    	}else if(condition.equals("country")){
	    		mid_sql = "select name, artist_id from artist where country='"+ keyword + "'";

	    	}

	    	mid_ps=(PreparedStatement)con.prepareStatement(mid_sql);
			mid_rs=mid_ps.executeQuery();

			while(mid_rs.next()){
				int artist_id = mid_rs.getInt("artist_id");
				String artist_name=mid_rs.getString("name");
				String url = "http://localhost:8080/hw1/artist_detail.jsp?artist_id="+artist_id;
				out.println("<a href='" + url + "'><h3>" + artist_name +"</h3></a>");
			}
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
