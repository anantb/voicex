package edu.stanford.voicex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
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
import edu.stanford.voicex.inbox.Status;

public class VoiceX{	
	String auth;
	String rnr_se;
	public VoiceX(String auth, String rnr_se){
		this.auth = auth;
		this.rnr_se = rnr_se;
		//InboxListenerThread inboxListener = new InboxListenerThread();
		//inboxListener.start();
	}
	
	
	
	public boolean sendSMS(String number, String text){
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("phoneNumber", number);		
		params.put("text", text);
		params.put("_rnr_se", rnr_se);		
		try{
	        URL url = Util.formURL(URLConstants.SMS_SEND_URL, null);	
	        HttpURLConnection conn = (HttpURLConnection) url.openConnection();       
	        conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);
	        conn.setDoOutput(true);
            OutputStreamWriter out = new OutputStreamWriter(conn.getOutputStream());
            out.write(Util.encodeURLPat(params));
            out.flush();            
            
	        BufferedReader reader=new BufferedReader(new InputStreamReader(conn.getInputStream()));
	        String line;  
	        String res="";	    		                
	        while ((line = reader.readLine()) != null) {
	        	res += line;		          
	        } 
	        Debug.print(res, Debug.VERBOSE);
	        Gson gson = new Gson() ;
			Status status =  gson.fromJson(res.toString(), Status.class);
			return status.isOk();
		}catch(Exception e){
			e.printStackTrace();
		}
		return false;       
	}
	
	public boolean call(String forwardingNumber, String outgoingNumber){
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("forwardingNumber", forwardingNumber);
		params.put("outgoingNumber", outgoingNumber);
		params.put("phoneType", "1");
		params.put("subscriberNumber", "undefined");
		params.put("remember", "0");
		params.put("_rnr_se", rnr_se);		
		try{
	        URL url = Util.formURL(URLConstants.CALL_INITIATE_URL, null);	
	        HttpURLConnection conn = (HttpURLConnection) url.openConnection();       
	        conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);
	        conn.setDoOutput(true);
            OutputStreamWriter out = new OutputStreamWriter(conn.getOutputStream());
            out.write(Util.encodeURLPat(params));
            out.flush();            
            
	        BufferedReader reader=new BufferedReader(new InputStreamReader(conn.getInputStream()));
	        String line;  
	        String res="";	    		                
	        while ((line = reader.readLine()) != null) {
	        	res += line;		          
	        } 
	        Debug.print(res, Debug.VERBOSE);
	        Gson gson = new Gson() ;
			Status status =  gson.fromJson(res.toString(), Status.class);
			return status.isOk();
		}catch(Exception e){
			e.printStackTrace();
		}
		return false;
	}
	
	public void sendSMSDelayed(String number, String text, long delay){		
		SMSRequestCollectorThread smsSenderThread = new SMSRequestCollectorThread(auth, number, text, delay);
		smsSenderThread.start();
		try{
			smsSenderThread.wait();
		}catch(InterruptedException ie){
			
		}		
	}
	
	public Inbox fetchInbox(){
		try{
			URL url = Util.formURL(URLConstants.SMS_URL, null);
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
		//Debug.print(json.toString(), Debug.VERBOSE);
		Gson gson = new Gson() ;
		Inbox inbox =  gson.fromJson(json.toString(), Inbox.class);
		if(inbox.getUnreadCounts().getSms() > 0){
			Messages messages = new Messages();
			
			JsonParser j = new JsonParser();
			JsonObject inboxObj = j.parse(json.toString()).getAsJsonObject();
			JsonObject messagesObj = inboxObj.get("messages").getAsJsonObject();
			Set<Entry<String, JsonElement>> entries = messagesObj.entrySet();
			Iterator<Entry<String, JsonElement>> itr = entries.iterator();
			while (itr.hasNext()) {
		        Map.Entry<String, JsonElement> entry = (Map.Entry<String, JsonElement>)itr.next();
		        MessageData msgData =  gson.fromJson(entry.getValue().toString(), MessageData.class);
		        //Debug.print(msgData.getMessageText(), Debug.VERBOSE);
		        messages.appendMessage(msgData);		        
		    }
			inbox.setMessages(messages);
		}
		return inbox;		
	}
	
	
	class InboxListenerThread extends Thread {
		public InboxListenerThread(){			
		}
		
		public void run() {
			Inbox inbox;
			Messages messsages;
			while(true){
				inbox = VoiceX.this.fetchInbox();
				if(inbox!=null){					
					if(inbox.getUnreadCounts().getSms() > 0){
						messsages = inbox.getMessages();
						for(int i=0; i<messsages.getMessages().size(); i++){
							if(messsages.getMessages().get(i).isRead() == false){
								System.out.println(messsages.getMessages().get(i).getMessageText());
							}
						}
					}
				}else{
					try{
						Thread.sleep(5000);
					}catch(InterruptedException ie){
						
					}
				}
			}
			
		}
		
	}

	
	

}


