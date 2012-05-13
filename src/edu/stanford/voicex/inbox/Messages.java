package edu.stanford.voicex.inbox;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class Messages {
	
	List<MessageData> messages;
	
	public Messages() {
		messages = new ArrayList<MessageData>(); 
	}
	
	public void appendMessage(MessageData msg) {
		messages.add(msg);
	}

	public List<MessageData> getMessages() {
		return messages;
	}

	public void setMessages(List<MessageData> messages) {
		this.messages = messages;
	}

	
	
	
	
}
