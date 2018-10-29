

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
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>EECS 118 File Uploading</title>

<style type="text/css">
h4{
	margin-bottom: 5px;
}

</style>

</head>
<body>
<a>Guru File Upload:</a>
Select file: <br />
<form method="post" enctype="multipart/form-data">
<input type="file" name="file" size="50" />
<h4>Title:</h4>
<input type="text" name="Title">
<h4>Year:</h4>
<input type="text" name="Year">
<h4>Artist:</h4>
<input type="text" name="Artist">
<h4>Brief Description:</h4>
<input type="text" name="Description">
<br />
<br />
<input type="submit" value="Submit" />
</form>
<%
   String baseUrl = "http://localhost:8080/";
   if(request != null){
       File file ;
	   int maxFileSize = 5000 * 1024;
	   int maxMemSize = 5000 * 1024;
	   String filePath = "/opt/tomcat/webapps/ROOT/";
	   String contentType = request.getContentType();
	   if ((contentType != null)&&(contentType.indexOf("multipart/form-data") >= 0)) {

	      DiskFileItemFactory factory = new DiskFileItemFactory();
	      factory.setSizeThreshold(maxMemSize);
	      factory.setRepository(new File("c:\\temp"));
	      ServletFileUpload upload = new ServletFileUpload(factory);
	      upload.setSizeMax( maxFileSize );
	      try{ 
	      	 
	         List fileItems = upload.parseRequest(request);
	         Iterator i = fileItems.iterator();

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
	                out.println("<img style='margin-top:30px' src='" + baseUrl + fileName + "'" + "/>");
	                out.println("<br/>");
	                out.println("<br/>");
	            }else{
	                String name = fi.getFieldName();
	                String value = fi.getString();
	                if(value.length() > 0){
	                	out.println("<h4>"+ name + ":" + value  + "<h4/>");
	            	}
            	}
	         }
	      }catch(Exception ex) {
	         System.out.println(ex);
	      }
	   }else{
	      out.println("<html>");
	      out.println("<body>");
	      out.println("<p>No file uploaded</p>"); 
	      out.println("</body>");
	      out.println("</html>");
	   }

	}
%>

</body>
</html>
