package edu.stanford.voicex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;

public class VoiceX{	
	String auth;
	
	public VoiceX(String auth_token){
		auth = auth_token;
		SMSReceiverThread smsReceiver = new SMSReceiverThread(auth);
		smsReceiver.start();
	}
	
	
	
	public boolean sendSMS(String number, String text){
		boolean status = false;
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("phoneNumber", number);		
		params.put("text", text);
		params.put("_rnr_se", "");	
		try{
	        URL url = Util.formURL(URLConstants.SMS_SEND_URL, params);
	
	        HttpURLConnection conn = (HttpURLConnection) url.openConnection();       
	        conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);
	        conn.connect();
	        BufferedReader reader;
	        String line;  
	        String res="";
	    	reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
	                
	        while ((line = reader.readLine()) != null) {
	        	res += line;		          
	        } 
	        Debug.print(res, Debug.VERBOSE);
	        if(res!=""){
	        	status = true;
	        }
		}catch(Exception e){
			
		}
		return status;       
	}
	
	public void call(String srcNum, String destNum){
		/*
		try{						
			voice.call(srcNum,destNum, "1");
		}catch(IOException ioe){
			ioe.printStackTrace();			
		}
		*/
	}
	
	public void sendSMSDelayed(String number, String text, long delay){		
		SMSSenderThread smsSenderThread = new SMSSenderThread(auth, number, text, delay);
		smsSenderThread.start();
		try{
			smsSenderThread.wait();
		}catch(InterruptedException ie){
			
		}		
	}
	
	

}


