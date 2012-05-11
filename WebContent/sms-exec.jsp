<%@ page import="edu.stanford.gvx.*, java.io.IOException;"%>
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
		GVX gvx = new GVX(login.getVoice());
		String number = request.getParameter("number");
		String text = request.getParameter("text");	
		long delay = 0;
		try{
			delay = Long.parseLong(request.getParameter("delay"));
		}catch(Exception e){
		}

		if(delay > 0){
			gvx.sendSMSDelayed(number, text, delay * 60 *1000);
			out.print("Message added to the server queue.");
		}else{
			if(gvx.sendSMS(number, text)){
				out.print("Message successfully sent.");	
			}else{
				out.print("Message sending failed.");	
			}
		}
		
	}
%>
<%@ include file="inc/footer.jsp" %>
