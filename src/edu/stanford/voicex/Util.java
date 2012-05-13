package edu.stanford.voicex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

public class Util {
	public static URL formURL(String base_url, HashMap<String, String> params) throws Exception{
		StringBuffer buf = new StringBuffer(base_url+"?");
		if(params != null){
			Iterator<Entry<String, String>> it = params.entrySet().iterator();
		    while (it.hasNext()) {
		        Map.Entry<String, String> param = (Map.Entry<String, String>)it.next();
		        buf.append(param.getKey() + "=" + URLEncoder.encode(param.getValue(), "UTF8"));
		        buf.append("&");
		    }
		}
	    buf.deleteCharAt(buf.length()-1);
	    URL url = new URL(buf.toString());
		return url;		
	}
	
	public static String fetch_get(URL url, String auth){		
		try{
			URLConnection conn = url.openConnection();
			conn.setRequestProperty( "Authorization", "GoogleLogin auth="+auth);          
			BufferedReader br= new BufferedReader(new InputStreamReader(conn.getInputStream()));
			StringBuffer buf = new StringBuffer("");
			String line;
			while ((line = br.readLine()) != null) {
			        buf.append(line + "\n\r");
			}
			br.close();
			return buf.toString();
		}catch(Exception e){
			return null;
		}
		
	}
}
