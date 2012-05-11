<%@ page import="edu.stanford.gvsms.*, java.io.IOException;"%>
<%@ include file="inc/header.jsp" %>
<%
    
    Config gv_config = new Config();
	Login login = null;
	try{
		login = new Login(gv_config);
	}catch(IOException ioe){	
		out.println("Login Failed");
	}
	if(login != null){		
		GVSMS gvSMS = new GVSMS(login.getVoice());
		String number = request.getParameter("number");
		String text = request.getParameter("text");	
		long delay = 0;
		try{
			delay = Long.parseLong(request.getParameter("delay"));
		}catch(Exception e){
		}

		if(delay > 0){
			gvSMS.sendSMSDelayed(number, text, delay * 60 *1000);
			out.print("Message added to the server queue.");
		}else{
			if(gvSMS.sendSMS(number, text)){
				out.print("Message successfully sent.");	
			}else{
				out.print("Message sending failed.");	
			}
		}
		out.print("<br />");
		out.print("<a href=\"index.jsp\">Click Here</a> to go back.");
	}
%>
<%@ include file="inc/footer.jsp" %>
