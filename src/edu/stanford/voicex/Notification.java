package edu.stanford.voicex;


import edu.stanford.voicex.inbox.MessageData;

public interface Notification {
	public void newNotification(MessageData msg);
}
