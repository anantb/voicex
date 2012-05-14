package edu.stanford.voicex;


import edu.stanford.voicex.inbox.MessageData;

public interface NewMessageCallback {
	public void newMsg(MessageData msg);
}
