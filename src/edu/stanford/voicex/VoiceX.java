package edu.stanford.voicex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


import edu.stanford.voicex.inbox.Inbox;
import edu.stanford.voicex.inbox.MessageData;
import edu.stanford.voicex.inbox.Messages;

public class VoiceX{	
	String auth;
	
	public VoiceX(String auth_token){
		auth = auth_token;
		InboxListenerThread inboxListener = new InboxListenerThread(auth);
		inboxListener.start();
	}
	
	
	
	public boolean sendSMS(String number, String text){
		boolean status = false;
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("phoneNumber", number);		
		params.put("text", text);
		params.put("_rnr_se", "");	
		try{
	        URL url = Util.formURL(URLConstants.SMS_URL, params);
	
	        HttpURLConnection conn = (HttpURLConnection) url.openConnection();       
	        conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);
	        conn.connect();
	        BufferedReader reader;
	        String line;  
	        String res="";
	    	reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
	                
	        while ((line = reader.readLine()) != null) {
	        	res += line;		          
	        } 
	        Debug.print(res, Debug.VERBOSE);
	        if(res!=""){
	        	status = true;
	        }
		}catch(Exception e){
			
		}
		return status;       
	}
	
	public void call(String srcNum, String destNum){
		/*
		try{						
			voice.call(srcNum,destNum, "1");
		}catch(IOException ioe){
			ioe.printStackTrace();			
		}
		*/
	}
	
	public void sendSMSDelayed(String number, String text, long delay){		
		SMSRequestCollectorThread smsSenderThread = new SMSRequestCollectorThread(auth, number, text, delay);
		smsSenderThread.start();
		try{
			smsSenderThread.wait();
		}catch(InterruptedException ie){
			
		}		
	}
	
	private Inbox fetch_inbox(URL url, String auth){		
		try{
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
			return inbox;
			
		}catch(Exception e){			
			e.printStackTrace();
			return null;
		}
		
	}
	
	
	class InboxListenerThread extends Thread {
		String auth;
		HashMap<String, String> params = new HashMap<String, String>();
		URL url;
		public InboxListenerThread(String auth){
			this.auth = auth;
			try{
				url = Util.formURL(URLConstants.SMS_URL, null);
			}catch(Exception e){
				
			}
		}
		
		public void run() {
			Inbox inbox;
			Messages messsages;
			while(true){
				inbox = VoiceX.this.fetch_inbox(url, auth);
				if(inbox!=null){
					messsages = inbox.getMessages();
					for(int i=0; i<messsages.getMessages().size(); i++){
						if(messsages.getMessages().get(i).isRead() == false){
							System.out.println(messsages.getMessages().get(i).getMessageText());
						}
					}
				}else{
					try{
						Thread.sleep(1000);
					}catch(InterruptedException ie){
						
					}
				}
			}
			
		}
		
	}

	
	

}


