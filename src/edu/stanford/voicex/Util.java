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
