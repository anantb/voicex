package edu.stanford.voicex;

import java.net.URL;
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
	
	
}
