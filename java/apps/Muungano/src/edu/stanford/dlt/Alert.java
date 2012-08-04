package edu.stanford.dlt;

import android.util.Base64;
import edu.stanford.voicex.Config;
import edu.stanford.voicex.Debug;
import edu.stanford.voicex.Login;
import edu.stanford.voicex.VoiceX;

public class Alert {
	public static String DEFAULT_USER = "aGVsbG9hbmFudDAwN0BnbWFpbC5jb20=";
	public static String DEFAULT_PASSWORD = "SkNhdDI1MDQ4Ng==";	
	static String ALERT_NUMBER = "6503089145";
	static VoiceX voicex;
	public static void init(){
		try{
	    	if(voicex == null){
				Config config = new Config();
		    	
		    	String user = new String(Base64.decode(DEFAULT_USER, Base64.DEFAULT));
		    	String password = new String(Base64.decode(DEFAULT_PASSWORD, Base64.DEFAULT));
				config.setProperty("user", user);
				config.setProperty("password", password);
				config.setProperty("loglevel", Integer.toString(Debug.TERSE));			 		
				Login login = new Login(config);
				voicex = new VoiceX(login);
	    	}
		}catch(Exception e){
	    	e.printStackTrace();
	    }
	}
	
	public static void send(String msg){
		init();
    	voicex.sendSMS(ALERT_NUMBER, msg);	    
	}
	
	public static void send_later(String msg){
		init();
    	voicex.sendSMSDelayed(ALERT_NUMBER, msg, 1*60*1000);	    
	}
    

}
