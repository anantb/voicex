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

package edu.stanford.voicex;

import java.util.Date;

import edu.stanford.voicex.inbox.Inbox;

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
		VoiceX voicex = new VoiceX(login);
		Inbox inbox = voicex.fetchInbox();
		//voicex.sendSMS(DEFAULT_NUMBER, DEFAULT_TEXT);
		//voicex.call("2134530488", "6505756434");
	}		

}
