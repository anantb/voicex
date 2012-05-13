package edu.stanford.voicex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;


public class Login{	
	final static String accountType = "google";
	final static String service = "grandcentral";
	final static String source = "voicex";
	
	String auth = null;
	public Login(Config config) throws Exception{	
		HashMap<String, String> params = new HashMap<String, String>();
		params.put("accountType", accountType);		
		params.put("Email", config.getProperty("user"));
		params.put("Passwd", config.getProperty("password"));
		params.put("service", service);
		params.put("source", source);
				
		URL url = Util.formURL(URLConstants.LOGIN_URL, params);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();	        
        conn.connect();
        int responseCode = conn.getResponseCode();	        
        BufferedReader reader;
        String line;
        if(responseCode==200) {
        	reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        } else {
        	reader = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
        }            
        while ((line = reader.readLine()) != null) {	            
	        if (line.contains("Auth=")) {
	        	this.auth = line.split("=", 2)[1].trim();	                    
	            Debug.print("Auth Success: " + auth, Debug.VERBOSE);	                    
	        } else if (line.contains("Error=")) {
	            String error = line.split("=", 2)[1].trim();
	            Debug.print("Auth Failed: " + error, Debug.VERBOSE);             
	        }        	
        } 
				
	}	
	
	public String getAuth() {	
		return auth;		
	}	
	
	
	
}


