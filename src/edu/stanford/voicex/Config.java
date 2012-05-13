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

import java.util.*;
import sun.misc.BASE64Decoder;
import java.io.IOException;

/**
 * @author Anant Bhardwaj
 * @date May 13, 2012
 *
 */
public class Config{
	public static String DEFAULT_USER = "dm9pY2V4LmdpdEBnbWFpbC5jb20=";
	public static String DEFAULT_PASSWORD = "Vm9pY2VYQEdpdA==";	
	
	Properties props = null;
	public Config(){
		props = new Properties();
		BASE64Decoder decoder = new BASE64Decoder();
		try{
			props.setProperty("user", new String(decoder.decodeBuffer(Config.DEFAULT_USER)));
			props.setProperty("password", new String(decoder.decodeBuffer(Config.DEFAULT_PASSWORD)));
			props.setProperty("loglevel", Integer.toString(Debug.VERBOSE));
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


