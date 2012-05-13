package edu.stanford.voicex;

import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

public class Util {
	public static String encodeURLPat(HashMap<String, String> params) throws Exception{
		StringBuffer buf = new StringBuffer();
		if(params != null){
			Iterator<Entry<String, String>> it = params.entrySet().iterator();
		    while (it.hasNext()) {
		        Map.Entry<String, String> param = (Map.Entry<String, String>)it.next();
		        buf.append(param.getKey() + "=" + URLEncoder.encode(param.getValue(), "UTF8"));
		        buf.append("&");
		    }
		}
		if(buf.toString().endsWith("&")){
			buf.deleteCharAt(buf.length()-1);
		}
	    return  buf.toString();
	}
	
	public static URL formURL(String baseURL, HashMap<String, String> params) throws Exception{
		String url = baseURL;
		if(params != null){
			String path = encodeURLPat(params);
			url = baseURL+"?"+path;
		}
		return new URL(url);
	}
	
	
}
