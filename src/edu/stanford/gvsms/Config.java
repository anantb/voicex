package edu.stanford.gvsms;

import java.util.*;
import sun.misc.BASE64Decoder;
import java.io.IOException;

public class Config{
	public static String DEFAULT_USER = "aGVsbG9hbmFudDAwN0BnbWFpbC5jb20=";
	public static String DEFAULT_PASSWORD = "SkNhdDI1MDQ4Ng==";	
	
	Properties props = null;
	public Config(){
		props = new Properties();
		BASE64Decoder decoder = new BASE64Decoder();
		try{
			props.setProperty("user", new String(decoder.decodeBuffer(Config.DEFAULT_USER)));
			props.setProperty("password", new String(decoder.decodeBuffer(Config.DEFAULT_PASSWORD)));
		}catch(IOException ioe){
		}
	}
	
	public void setProperty(String k, String v){
		props.setProperty(k, v);		
	}
	
	public String getProperty(String k){
		return props.getProperty(k, "");		
	}
	
	
}


