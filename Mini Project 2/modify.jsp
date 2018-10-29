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
	<%

	if(request != null){
		String from = request.getParameter("from");
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

	    ResultSet rs = null;
		if(from.equals("gallery_modify")){
			int gallery_id = Integer.parseInt(request.getParameter("g_id"));
			String newName = request.getParameter("Name");
			String newDes = request.getParameter("Description");
			String ud_gallery = "update gallery set name=?, description=? where gallery_id=?";
		    if(!con.isClosed()){
				PreparedStatement up_pstmt = con.prepareStatement(ud_gallery,Statement.RETURN_GENERATED_KEYS);
				up_pstmt.setString(1, newName);
	            up_pstmt.setString(2, newDes);
	            up_pstmt.setInt(3, gallery_id);
	            up_pstmt.executeUpdate();
	            out.println("Gallery modified!");
		    }else{
		      out.println("Database Not Connected!");
		    }

		}else if(from.equals("img_detail")){
			String title = request.getParameter("Title");
			String link = request.getParameter("Link");
			int year = Integer.parseInt(request.getParameter("Year"));
			String type = request.getParameter("Type");
			int width = Integer.parseInt(request.getParameter("Width"));
			int height = Integer.parseInt(request.getParameter("Height"));
			String location = request.getParameter("Location");
			String des = request.getParameter("Description");
			int img_id = Integer.parseInt(request.getParameter("img_id"));

			String ud_img_dt = "update detail set year=?,type=?,width=?,height=?,location=?,description=? where image_id=?";

			String ud_img = "update image set title=?,link=? where image_id=?";
			
			if(!con.isClosed()){
				PreparedStatement up_img_dt = con.prepareStatement(ud_img_dt,Statement.RETURN_GENERATED_KEYS);
				
	            up_img_dt.setInt(1, year);
	            up_img_dt.setString(2, type);
	            up_img_dt.setInt(3, width);
	            up_img_dt.setInt(4, height);
	            up_img_dt.setString(5, location);
	            up_img_dt.setString(6, des);
	            up_img_dt.setInt(7, img_id);
	            up_img_dt.executeUpdate();

	            PreparedStatement up_img = con.prepareStatement(ud_img,Statement.RETURN_GENERATED_KEYS);
	            up_img.setString(1, title);
	            up_img.setString(2, link);
	            up_img.setInt(3, img_id);
	            up_img.executeUpdate();

	          	out.println("Image modified!");

		    }else{
		      out.println("Database Not Connected!");
		    }
		}else if(from.equals("artist_detail")){
			int artist_id = Integer.parseInt(request.getParameter("artist_id"));
			String newName = request.getParameter("Name");
			int newby = Integer.parseInt(request.getParameter("Birthyear"));
			String newCountry = request.getParameter("Country");
			String newDes = request.getParameter("Description");
			String ud_artist = "update artist set name=?,birth_year=?,country=?,description=? where artist_id=?";
		    if(!con.isClosed()){
				PreparedStatement up_pstmt_art = con.prepareStatement(ud_artist,Statement.RETURN_GENERATED_KEYS);
				up_pstmt_art.setString(1, newName);
	            up_pstmt_art.setInt(2, newby);
	            up_pstmt_art.setString(3, newCountry);
	            up_pstmt_art.setString(4, newDes);
	            up_pstmt_art.setInt(5, artist_id);
	            up_pstmt_art.executeUpdate();
	            out.println("Artist modified!");
		    }else{
		      out.println("Database Not Connected!");
		    }
		}
	}

%>




</body>


</html>
