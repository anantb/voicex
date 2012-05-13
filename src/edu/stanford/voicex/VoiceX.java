package edu.stanford.voicex;

import java.io.IOException;
import java.util.*;

import com.techventus.server.voice.Voice;


public class VoiceX{	
	static String DEFAULT_NUMBER = "6503088677";
	static String DEFAULT_TEXT = "Test SMS Generated at: " +  new Date();
	Voice voice = null;
	
	public VoiceX(Voice v){	
		voice = v;		
	}
	
	public static void main(String[] args) throws IOException{	
		Config config = new Config();
		Login login = null;
		try{
			login = new Login(config);
		}catch(IOException ioe){			
			System.err.println("Authentication Failed");
			System.exit(-1);
		}
				
		VoiceX voicex = new VoiceX(login.getVoice());		
		voicex.sendSMS(DEFAULT_NUMBER, DEFAULT_TEXT);
	}	
		
	
	public boolean sendSMS(String number, String text){
		try{						
			voice.sendSMS(number,text);
			return true;
		}catch(IOException ioe){
			ioe.printStackTrace();
			return false;
		}
	}
	
	public void sendSMSDelayed(String number, String text, long delay){
		SMSThread smsThread = new SMSThread(voice, number, text, delay);
		smsThread.start();
	}
	
	
	class SMSThread extends Thread {
		Voice voice = null;
		String number = null;
		String text = null;
		long delay = 0;
		boolean status = false;
		
		public SMSThread(Voice voice, String number, String text, long delay){
			this.voice = voice;
			this.number = number;
			this.text = text;
			this.delay  = delay;
		}
		
		public void run() {
			try{
				try{
					Thread.sleep(delay);
				}catch(InterruptedException ie){
				}			
				voice.sendSMS(number, text);
				status = true;
			}catch(IOException ioe){
				ioe.printStackTrace();
				status = false;
			}
		}
	}
}


