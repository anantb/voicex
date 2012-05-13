package edu.stanford.voicex.inbox;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class MessageData {
	String id;
	String phoneNumber;
	String displayNumber;
	String startTime;
	String displayStartDateTime;
	String displayStartTime;
	String relativeStartTime;
	String note;
	boolean isRead;
	boolean isSpam;
	boolean isThrash;
	boolean star;
	String messageText;
	String[] labels;
	String type;
	String children;
	
	public String getId() {
		return id;
	}
	
	public void setId(String id) {
		this.id = id;
	}
	
	public String getPhoneNumber() {
		return phoneNumber;
	}
	
	public void setPhoneNumber(String phoneNumber) {
		this.phoneNumber = phoneNumber;
	}
	
	public String getDisplayNumber() {
		return displayNumber;
	}
	
	public void setDisplayNumber(String displayNumber) {
		this.displayNumber = displayNumber;
	}
	
	public String getStartTime() {
		return startTime;
	}
	
	public void setStartTime(String startTime) {
		this.startTime = startTime;
	}
	
	public String getDisplayStartDateTime() {
		return displayStartDateTime;
	}
	
	public void setDisplayStartDateTime(String displayStartDateTime) {
		this.displayStartDateTime = displayStartDateTime;
	}
	
	public String getDisplayStartTime() {
		return displayStartTime;
	}
	
	public void setDisplayStartTime(String displayStartTime) {
		this.displayStartTime = displayStartTime;
	}
	
	public String getRelativeStartTime() {
		return relativeStartTime;
	}
	
	public void setRelativeStartTime(String relativeStartTime) {
		this.relativeStartTime = relativeStartTime;
	}
	
	public String getNote() {
		return note;
	}
	
	public void setNote(String note) {
		this.note = note;
	}
	
	
	
	public boolean isRead() {
		return isRead;
	}

	public void setRead(boolean isRead) {
		this.isRead = isRead;
	}

	public boolean isSpam() {
		return isSpam;
	}

	public void setSpam(boolean isSpam) {
		this.isSpam = isSpam;
	}

	public boolean isThrash() {
		return isThrash;
	}

	public void setThrash(boolean isThrash) {
		this.isThrash = isThrash;
	}

	public boolean isStar() {
		return star;
	}

	public void setStar(boolean star) {
		this.star = star;
	}

	public String getMessageText() {
		return messageText;
	}
	
	public void setMessageText(String messageText) {
		this.messageText = messageText;
	}
	
	public String[] getLabels() {
		return labels;
	}
	
	public void setLabels(String[] labels) {
		this.labels = labels;
	}
	
	public String getType() {
		return type;
	}
	
	public void setType(String type) {
		this.type = type;
	}
	
	public String getChildren() {
		return children;
	}
	
	public void setChildren(String children) {
		this.children = children;
	}
	
	
}