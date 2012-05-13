package edu.stanford.voicex.inbox;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class Inbox {
	Messages messages;
	int totalSize;
	UnreadCounts unreadCounts;
	int resultsPerPage;
	
	public Messages getMessages() {
		return messages;
	}
	public void setMessages(Messages messages) {
		this.messages = messages;
	}
	public int getTotalSize() {
		return totalSize;
	}
	public void setTotalSize(int totalSize) {
		this.totalSize = totalSize;
	}
	public UnreadCounts getUnreadCounts() {
		return unreadCounts;
	}
	public void setUnreadCounts(UnreadCounts unreadCounts) {
		this.unreadCounts = unreadCounts;
	}
	public int getResultsPerPage() {
		return resultsPerPage;
	}
	public void setResultsPerPage(int resultsPerPage) {
		this.resultsPerPage = resultsPerPage;
	}
	
	
	
	

	
	
}
