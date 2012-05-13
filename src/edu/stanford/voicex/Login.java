package edu.stanford.voicex;

import java.io.IOException;
import com.techventus.server.voice.Voice;


public class Login{
	Voice voice = null;
	public Login(Config config) throws IOException{		
		voice = new Voice(config.getProperty("user"), config.getProperty("password"),"GoogleVoiceJava",true,Voice.GOOGLE);		
	}	
	
	public Voice getVoice() {	
		return voice;		
	}	
	
}


