package edu.stanford.voicex;

import java.util.Date;

public class TestVoiceX {
	static String DEFAULT_NUMBER = "6503088677";
	static String DEFAULT_TEXT = "Test SMS Generated at: " +  new Date();
	
	public static void main(String[] args) {		
		Config config = new Config();
		Login login = null;
		try{
			login = new Login(config);
		}catch(Exception ioe){			
			System.err.println("Authentication Failed");
			System.exit(-1);
		}				
		VoiceX voicex = new VoiceX(login.getAuth());		
		//voicex.sendSMS(DEFAULT_NUMBER, DEFAULT_TEXT);
		//voicex.call("6505756434", "2134530488");
	}		

}
