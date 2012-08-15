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

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */

public class Login{	
	final static String accountType = "google";
	final static String service = "grandcentral";
	final static String source = "voicex";
	
	String auth = null;
	String rnr_se = null;
	Config config = null;
	
	public Login(Config config) throws Exception{	
		this.config = config;
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
	            initialize();
	        } else if (line.contains("Error=")) {
	            String error = line.split("=", 2)[1].trim();
	            Debug.print("Auth Failed: " + error, Debug.VERBOSE);             
	        }        	
        } 
				
	}
	
	public String getAuth() {	
		return auth;		
	}
	
	public Config getConfig() {	
		return config;		
	}
	
	public String getRNRSE(){
		return rnr_se;
	}
	
	private void initialize() throws Exception{
		URL url = Util.formURL(URLConstants.ROOT_URL, null);		
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();       
        conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);
        conn.connect();
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String line;  
        while((line=reader.readLine()) != null){
        	 if(line.contains("'_rnr_se': '")) {
                 String tokens = line.split("'_rnr_se': '", 2)[1];
                 this.rnr_se = tokens.split("',", 2)[0];
                 Debug.print("RNRSE: " + rnr_se, Debug.VERBOSE);
                 return;
        	 }
        	
        }
				
	}	
	
	
	
}


