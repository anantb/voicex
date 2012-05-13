package edu.stanford.voicex;

import java.net.URL;
import java.util.HashMap;

public class SMSReceiverThread extends Thread {
	String auth;
	HashMap<String, String> params = new HashMap<String, String>();
	URL url;
	public SMSReceiverThread(String auth){
		this.auth = auth;
		try{
			url = Util.formURL(URLConstants.UNREAD_URL, null);
		}catch(Exception e){
			
		}
	}
	
	public void run() {			
		String new_sms = Util.fetch_get(url, auth);
		if(new_sms!=null){
			System.out.println(new_sms);
		}else{
			try{
				Thread.sleep(1000);
			}catch(InterruptedException ie){
				
			}
		}
		
	}
	
}
