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


import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.Map.Entry;
import java.util.Set;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


import edu.stanford.voicex.inbox.Inbox;
import edu.stanford.voicex.inbox.MessageData;
import edu.stanford.voicex.inbox.Messages;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */

public class VoiceX{	
	String auth;
	String rnr_se;
	Config config;
	InboxListenerThread inboxListener;
	Timer timer;
	public VoiceX(Login login){
		this.auth = login.getAuth();
		this.rnr_se = login.getRNRSE();
		this.config = login.getConfig();
		inboxListener = new InboxListenerThread();
		inboxListener.start();
		timer = new Timer();
	}
	
	
	
	public boolean sendSMS(String number, String text){
		Debug.print("Sending msg to: "+number, Debug.VERBOSE);
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("phoneNumber", number);		
		params.put("text", text);
		params.put("_rnr_se", rnr_se);		
		//return Util.doPost(URLConstants.SMS_SEND_URL, params, auth);
		return true;
	}
	
	public boolean call(String forwardingNumber, String outgoingNumber){
		Debug.print("Initiating call to: "+outgoingNumber + ", through: " + forwardingNumber, Debug.VERBOSE);
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("forwardingNumber", forwardingNumber);
		params.put("outgoingNumber", outgoingNumber);
		params.put("phoneType", "1");
		params.put("subscriberNumber", "undefined");
		params.put("remember", "0");
		params.put("_rnr_se", rnr_se);		
		return Util.doPost(URLConstants.CALL_INITIATE_URL, params, auth);
		
	}
	
	
	public boolean markAsRead(MessageData msg){
		Debug.print("Marking Msg as Read: "+msg.getMessageText(), Debug.VERBOSE);
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("messages", msg.getId());
		params.put("read", "1");
		params.put("_rnr_se", rnr_se);		
		return Util.doPost(URLConstants.MSG_MARK_READ_URL, params, auth);
	}
	
	
	public boolean markAsUnRead(MessageData msg){
		Debug.print("Marking Msg as UnRead: "+msg.getMessageText(), Debug.VERBOSE);
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("messages", msg.getId());
		params.put("read", "0");
		params.put("_rnr_se", rnr_se);		
		return Util.doPost(URLConstants.MSG_MARK_READ_URL, params, auth);
	}
	
	public boolean delete(MessageData msg){
		Debug.print("Deleting Msg:: "+msg.getMessageText(), Debug.VERBOSE);
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("messages", msg.getId());
		params.put("trash", "1");
		params.put("_rnr_se", rnr_se);		
		return Util.doPost(URLConstants.MSG_DELETE_URL, params, auth);
	}
	
	public void sendSMSDelayed(String number, String text, long delay){	
		Debug.print("Scheduling delayed SMS: "+number, Debug.VERBOSE);
		ScheduledSMS scheduledSMS = new ScheduledSMS(VoiceX.this, number, text);
		this.timer.schedule(scheduledSMS, delay);	
	}
	
	public void registerNotification(Notifiee notification){
		this.inboxListener.addNotifiee(notification);		
	}
	
	public void removeNotification(Notifiee notification){
		this.inboxListener.deleteNotifiee(notification);		
	}
	
	public Inbox fetchInbox(){
		try{
			URL url = Util.formURL(URLConstants.INBOX_URL, null);
			return fetchInbox(url, auth);
		}catch(Exception e){
			return null;
		}		
		
	}
	
	public Inbox fetchAllSMS(){
		try{
			URL url = Util.formURL(URLConstants.SMS_URL, null);
			return fetchInbox(url, auth);
		}catch(Exception e){
			return null;
		}		
		
	}
	
	public Inbox fetchUnreadSMS(){
		try{
			URL url = Util.formURL(URLConstants.SMS_UNREAD_URL, null);
			return fetchInbox(url, auth);
		}catch(Exception e){
			return null;
		}		
		
	}
	
	private Inbox fetchInbox(URL url, String auth) throws Exception{		
		URLConnection conn = url.openConnection();
		conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);          
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		Document doc = dBuilder.parse(conn.getInputStream());
		NodeList nodes = doc.getElementsByTagName("json");		
		StringBuffer json = new StringBuffer(nodes.item(0).getTextContent());		
		Debug.print(json.toString(), Debug.VERBOSE);
		Gson gson = new Gson() ;
		Inbox inbox =  gson.fromJson(json.toString(), Inbox.class);
		
		Messages messages = new Messages();
		
		JsonParser j = new JsonParser();
		JsonObject inboxObj = j.parse(json.toString()).getAsJsonObject();
		JsonObject messagesObj = inboxObj.get("messages").getAsJsonObject();
		Set<Entry<String, JsonElement>> entries = messagesObj.entrySet();
		Iterator<Entry<String, JsonElement>> itr = entries.iterator();
		while (itr.hasNext()) {
	        Map.Entry<String, JsonElement> entry = (Map.Entry<String, JsonElement>)itr.next();
	        MessageData msgData =  gson.fromJson(entry.getValue().toString(), MessageData.class);
	        messages.appendMessage(msgData);		        
	    }
		inbox.setMessages(messages);
		
		return inbox;		
	}
	
	
	
	
	
	class InboxListenerThread extends Thread {
		HashMap<String, Notifiee> notifiees;
		public InboxListenerThread(){
			notifiees = new HashMap<String, Notifiee>();
		}
		
		public void addNotifiee(Notifiee notifiee){
			notifiees.put(notifiee.toString(), notifiee);
		}
		
		public void deleteNotifiee(Notifiee notifiee){
			notifiees.remove(notifiee.toString());
		}
		
		public void notify(MessageData msg){
			Iterator<Entry<String, Notifiee>> itr = notifiees.entrySet().iterator();
		    while (itr.hasNext()) {
		        Map.Entry<String, Notifiee> cb = (Map.Entry<String, Notifiee>)itr.next();
		        try{
		        	cb.getValue().notificationNew(msg);
		        }catch(NullPointerException npe){
		        	this.deleteNotifiee(cb.getValue());
		        }catch(Exception e){
		        	
		        }
		    }		    
		}
		
		public void run() {			
			while(true){
				Inbox inbox = VoiceX.this.fetchUnreadSMS();									
				if(inbox!=null && inbox.getUnreadCounts().getSms() > 0){
					List<MessageData> msgList = inbox.getMessages().getList();
					for(int i=0; i<msgList.size(); i++){
						if(msgList.get(i).isRead() == false){
							MessageData msg = msgList.get(i);					
							notify(msg);	
						}
					}
				}
				try{
					Thread.sleep(5000);
				}catch(InterruptedException ie){}				
				
			
			}	
		}
		
		
		
		
	}
	

}


