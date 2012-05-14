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

import edu.stanford.voicex.Debug;
import edu.stanford.voicex.Notifiee;
import edu.stanford.voicex.VoiceX;
import edu.stanford.voicex.inbox.MessageData;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */
public class Alert implements Notifiee{
	static String ALERT_NUMBER = "6503088677";
	static String DEFAULT_TEXT = "Alert from: ";
	VoiceX v;
	public Alert(VoiceX v){
		this.v = v;
		v.registerNotification(this);
	}
	public void notificationNew(MessageData msg){
		Debug.print("Got a notification", Debug.VERBOSE);
		v.sendSMS(ALERT_NUMBER, DEFAULT_TEXT+msg.getPhoneNumber());
		v.markAsRead(msg);
	}
}
