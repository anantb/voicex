package edu.stanford.voicex;

public class SMSSenderThread extends Thread {
	String auth;
	String number;
	String text;
	long delay = 0;		
	
	public SMSSenderThread(String auth, String number, String text, long delay){
		this.auth = auth;
		this.number = number;
		this.text = text;
		this.delay  = delay;
	}
	
	public void run() {		
		try{
			Thread.sleep(delay);
		}catch(InterruptedException ie){
		}			
		//voice.sendSMS(number, text);		
		this.notify();
	}
}
