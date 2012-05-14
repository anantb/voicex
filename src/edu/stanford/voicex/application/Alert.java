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
package edu.stanford.voicex.application;

import java.util.Date;

import edu.stanford.voicex.Config;
import edu.stanford.voicex.Login;
import edu.stanford.voicex.NewMessageCallback;
import edu.stanford.voicex.VoiceX;
import edu.stanford.voicex.inbox.Inbox;
import edu.stanford.voicex.inbox.MessageData;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */
public class Alert {
	static String ALERT_NUMBER = "6503088677";
	static String DEFAULT_TEXT = "Alert from: ";
	public Alert(){		
	}
	public static void main(String[] args) {		
		Alert alert = new Alert();
		Config config = new Config();
		Login login = null;
		try{
			login = new Login(config);
		}catch(Exception ioe){			
			System.err.println("Authentication Failed");
			System.exit(-1);
		}				
		VoiceX voicex = new VoiceX(login);
		NewMessageCallback msgHandler = alert.new NewMessageHandler(voicex);
		voicex.registerNewMessageCallback(msgHandler);
	}
	
	class NewMessageHandler implements NewMessageCallback{
		VoiceX v;
		public NewMessageHandler(VoiceX v){
			this.v = v;
		}
		public void newMsg(MessageData msg){
			v.sendSMS(ALERT_NUMBER, DEFAULT_TEXT+msg.getPhoneNumber());
			v.markAsRead(msg);
		}
	}

}
