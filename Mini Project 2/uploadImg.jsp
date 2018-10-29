
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
	  File file ;
      int maxFileSize = 5000 * 1024;
      int maxMemSize = 5000 * 1024;
      String filePath = "/opt/tomcat/webapps/ROOT/";
      String contentType = request.getContentType();
      String baseUrl = "http://localhost:8080/";
      Connection con = DriverManager.getConnection(dbUrl,id,pwd);

      if ((contentType != null)&&(contentType.indexOf("multipart/form-data") >= 0)) {
        DiskFileItemFactory factory = new DiskFileItemFactory();
        factory.setSizeThreshold(maxMemSize);
        factory.setRepository(new File("c:\\temp"));
        ServletFileUpload upload = new ServletFileUpload(factory);
        upload.setSizeMax( maxFileSize );
        try{
           	List fileItems = upload.parseRequest(request);
           	Iterator i = fileItems.iterator();
            String imgurl = "";
            String imgTitle = "";
            String artist = "";
            String year = "";
            String type = "";
            String location = "";
            String description = "";
           	while ( i.hasNext () ) 
           	{
              FileItem fi = (FileItem)i.next();


              if (!fi.isFormField()){
                  String fieldName = fi.getFieldName();
                  String fileName = fi.getName();
                  boolean isInMemory = fi.isInMemory();
                  long sizeInBytes = fi.getSize();
                  file = new File( filePath + fileName) ;
                  fi.write( file ) ;
                  imgurl = baseUrl + fileName;
                  out.println("<img style='margin-top:30px' src='" + imgurl + "'" + "/>");
                  out.println("<br/>");
                  out.println("<br/>");
              }else{
                  String name = fi.getFieldName();
                  String value = fi.getString();
                  if(name.equals("Title")){
                    imgTitle = value;
                  }else if(name.equals( "Year")){
                    year = value;
                  }else if(name.equals( "Artist")){
                    artist = value;
                  }else if(name.equals( "Type")){
                    type = value;
                  }else if(name.equals( "Location")){
                    location = value;
                  }else if(name.equals( "Description")){
                    description = value;
                  }
              	}
              
           	}
          out.println(year + ":" + imgTitle);

          String sel_art_id = "select artist_id from artist where name=";
          PreparedStatement upload_ps=(PreparedStatement)con.prepareStatement(sel_art_id);
          ResultSet upload_rs=upload_ps.executeQuery();
          int artist_id = 0;
          while(upload_rs.next()){
            artist_id = upload_rs.getInt("artist_id");
          }

          PreparedStatement up_pstmt = con.prepareStatement("insert into detial values(default,?,?,?,?,?,?,?)",Statement.RETURN_GENERATED_KEYS);
          up_pstmt.setString(1, null);
          up_pstmt.setString(2, year);
          up_pstmt.setString(3, type);
          up_pstmt.setInt(4, 100);
          up_pstmt.setInt(5, 100);
          up_pstmt.setString(6, location);
          up_pstmt.setString(7, description);

          up_pstmt.executeUpdate();
          upload_rs=up_pstmt.getGeneratedKeys();
          int detail_id = 0;
          while (upload_rs.next()) {
            detail_id = upload_rs.getInt(1);
          }

          String ins_img = "insert into image values(default,?,?,?,?,?)";

          up_pstmt = con.prepareStatement(ins_img,Statement.RETURN_GENERATED_KEYS);
          up_pstmt.clearParameters();
          up_pstmt.setString(1, imgTitle);
          up_pstmt.setString(2, imgurl);
          up_pstmt.setInt(3, Integer.parseInt(gallery_id));
          up_pstmt.setInt(4, artist_id);
          up_pstmt.setInt(5, detail_id);
          up_pstmt.executeUpdate();

          out.println(imgurl, imgTitle);
        }catch(Exception ex) {
           System.out.println(ex);
        }
     }


	%>


	<button id="myBtn" name="create">Create Gallery</button>
	<button>Create Artists</button>

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

</script>

</body>


