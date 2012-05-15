/*
Copyright (c) 2012 Anant Bhardwaj

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
package edu.stanford.voicex.applications;

import sun.misc.BASE64Decoder;
import edu.stanford.voicex.Config;
import edu.stanford.voicex.Debug;
import edu.stanford.voicex.Login;
import edu.stanford.voicex.Notifiee;
import edu.stanford.voicex.VoiceX;
import edu.stanford.voicex.inbox.MessageData;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */
public class Alert implements Notifiee{
	// Replace it with you google account username and password.
	public static String DEFAULT_USER = "dm9pY2V4LmdpdEBnbWFpbC5jb20=";
	public static String DEFAULT_PASSWORD = "Vm9pY2VYQEdpdA==";	
	static String ALERT_NUMBER = "6503088677";
	static String DEFAULT_TEXT = "New Message: ";
	
	VoiceX voicex;
	
	public Alert(){	
		init();
		voicex.registerNotification(this);		
	}	
	
	public void notificationNew(MessageData msg){
		Debug.print("Got a notification", Debug.VERBOSE);
		voicex.sendSMS(ALERT_NUMBER, 
				DEFAULT_TEXT + msg.getMessageText() + ". " + 
				"From: " + msg.getPhoneNumber());
		voicex.markAsRead(msg);
	}
	
	
	void init(){		
		try{
			BASE64Decoder decoder = new BASE64Decoder();
			Config config = new Config();
			config.setProperty("user", new String(decoder.decodeBuffer(DEFAULT_USER)));
			config.setProperty("password", new String(decoder.decodeBuffer(DEFAULT_PASSWORD)));
			config.setProperty("loglevel", Integer.toString(Debug.VERBOSE));			 		
			Login login = new Login(config);
			voicex = new VoiceX(login);
		}catch(Exception e){			
			System.err.println("Authentication Failed");
			System.exit(-1);
		}		
				
	}
}
