

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
<link href="style.css" rel="stylesheet">
</head>
<body>


<%
    int count = 0;
    if(request != null){
      
      String sql_select = "select * from %s";
      String sql_insert = "insert into gallery values(default, ?, ?)";
      String gallery_id = "";

      String galleryName = request.getParameter("gName");
      
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

      if(request.getParameter("existed") == null){
        String description = request.getParameter("Description");
        out.println(galleryName + ":" + description); 

        if(!con.isClosed()){
          out.println("Connected!");
          PreparedStatement pstmt = con.prepareStatement(sql_insert,Statement.RETURN_GENERATED_KEYS);
          pstmt.clearParameters();
          pstmt.setString(1, galleryName);
          pstmt.setString(2, description);
          pstmt.executeUpdate();
          ResultSet rs=pstmt.getGeneratedKeys();
          out.println(rs.toString());
          while (rs.next()) {
            out.println("Successfully added. Customer_ID:"+rs.getInt(1));
          }

        }else{
          out.println("Database Not Connected!");
        }

      }else{

        gallery_id = request.getParameter("gallery_id");
        String select_img = "select * from image where gallery_id=" + gallery_id;
        PreparedStatement ps=(PreparedStatement)con.prepareStatement(select_img);

        if(!con.isClosed()){
            
            ResultSet rs=ps.executeQuery();
            while(rs.next()){
              String img_title=rs.getString("title");
              String get_img_id = rs.getString("image_id");

              String link = rs.getString("link");

              String img_link = "http://localhost:8080/hw1/image_detail.jsp?img_id=" + get_img_id;

              out.println("<div class='responsive'><div class='gallery'><a target='_blank' href='" + img_link +"'><img src='"+ link +"' alt='Mountains' width='600' height='400'></a><div class='desc'>"+ img_title +"</div></div></div>");
              count ++;
              out.println("</br>");
            }
          
          out.println(gallery_id);
          out.println("<div id='modifyWindow' class='modal'> <div class='modal-content'> <span class='modclose'>&times;</span> <form action='modify.jsp' method='post'> <h4>Name:</h4> <input type='text' name='Name'> <h4>Description:</h4> <input type='text' name='Description'> <input type='hidden' name='from' value='gallery_modify'> <input type='hidden' name='g_id' value='"+ gallery_id +"'> <br /> <br /> <input type='submit' value='Submit' /> </form> </div></div>");  

        }else{
          out.println("Database Not Connected!");
        }
      }



      File file ;
      int maxFileSize = 5000 * 1024;
      int maxMemSize = 5000 * 1024;
      String filePath = "/opt/tomcat/webapps/ROOT/";
      String contentType = request.getContentType();
      String baseUrl = "http://localhost:8080/";

      int height = 0;
      int width = 0;

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
            int year = 0;
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
                    year = Integer.parseInt(value);
                  }else if(name.equals( "Artist")){
                    artist = value;
                  }else if(name.equals( "Type")){
                    type = value;
                  }else if(name.equals( "Location")){
                    location = value;
                  }else if(name.equals( "Description")){
                    description = value;
                  }else if(name.equals( "Height")){
                    height = Integer.parseInt(value);
                  }else if(name.equals( "Width")){
                    width = Integer.parseInt(value);
                  
                  }
              }
              
          }



          String sel_art_id = "select artist_id from artist where name='" + artist + "'";

          PreparedStatement upload_ps=(PreparedStatement)con.prepareStatement(sel_art_id);

          ResultSet upload_rs=upload_ps.executeQuery();
          int artist_id = -1;
          while(upload_rs.next()){
            artist_id = upload_rs.getInt("artist_id");
            out.println("artist:" + artist_id);
          }


          if(artist_id < 0){
            out.println("Invalid artist name, must have been added!\n");
          }else{
            PreparedStatement up_pstmt = con.prepareStatement("insert into detail values(default,?,?,?,?,?,?,?)",Statement.RETURN_GENERATED_KEYS);
            up_pstmt.setString(1, null);
            up_pstmt.setInt(2, year);
            up_pstmt.setString(3, type);
            up_pstmt.setInt(4, width);
            up_pstmt.setInt(5, height);
            up_pstmt.setString(6, location);
            up_pstmt.setString(7, description);

            int detail_id = 0;
            up_pstmt.executeUpdate();
            ResultSet detail_rs=up_pstmt.getGeneratedKeys();

            while (detail_rs.next()) {
              detail_id = detail_rs.getInt(1);
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

            ResultSet img_rs = up_pstmt.getGeneratedKeys();
            int img_id = 0;
            while (img_rs.next()) {
              img_id = img_rs.getInt(1);
            }

            String sql_update_detail = "update detail set image_id=? where detail_id=?";

            upload_ps=(PreparedStatement)con.prepareStatement(sql_update_detail);
            upload_ps.setInt(1, img_id);
            upload_ps.setInt(2, detail_id);

            int c = upload_ps.executeUpdate();
            out.println(c);
          }

        }catch(Exception ex) {
           System.out.println(ex);
        }
     }
    
    out.println("<div class='countContainer'>Image Count: " + count + "</div>");

  }
  
%>

       <button id='myBtn' class='uploadButton' name='create'>Upload Image</button>
      <button id='modify' class='modifyButton' name='create'>Modify Gallery</button>
  <!-- The Modal -->
  <div id="myModal" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
      <span class="close">&times;</span>
      <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" size="50" />

      <h4>Title:</h4>
      <input type="text" name="Title">

      <h4>Year:</h4>
      <input type="text" name="Year">

      <h4>Artist:</h4>
      <input type="text" name="Artist">

      <h4>Type:</h4>
      <input type="text" name="Type">

      <h4>Width:</h4>
      <input type="text" name="Width">

      <h4>Height:</h4>
      <input type="text" name="Height">

      <h4>location:</h4>
      <input type="text" name="Location">

      <h4>Brief Description:</h4>
      <input type="text" name="Description">
      <br />
      <br />
      <input type="submit" value="Submit" />
      </form>
    </div>
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
  var modspan = document.getElementsByClassName("modclose")[0];
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