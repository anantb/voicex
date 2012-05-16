package edu.stanford.voicex.db;

import java.net.URLEncoder;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import edu.stanford.voicex.Debug;

import sun.misc.BASE64Decoder;


public class Subscription {
	static Connection con;
	static Statement st;
    static HashMap<String, String> sub_unchanged = new HashMap<String, String>();
    static HashMap<String, String> sub_dirty = new HashMap<String, String>();
    

	public static void load(){
		try{
			connect();			
			ResultSet rs = st.executeQuery("SELECT * FROM subscription");
	
			while (rs.next()) {				
				sub_unchanged.put(rs.getString(1), rs.getString(2));
			}
		}catch(SQLException sqe){
			sqe.printStackTrace();
		}catch(Exception e){
			e.printStackTrace();
		}
  
	}
	
	public static void add(String number, String subscription){
		
		if(sub_unchanged.get(number.trim()) != null){
			sub_unchanged.remove(number.trim());
		}
		sub_dirty.put(number.trim(), subscription.trim());
	}
	
	public static String find(String number){
		String subscription;		
		subscription = sub_dirty.get(number.trim());	
		if(subscription == null){
			subscription = sub_unchanged.get(number.trim());
		}
		return subscription;
	}
	
	public static void save(){
		try{
			connect();		
			Iterator<Entry<String, String>> it_dirty = sub_dirty.entrySet().iterator();
		    while (it_dirty.hasNext()) {
		        Map.Entry<String, String> row = (Map.Entry<String, String>)it_dirty.next();		        
		        st.executeUpdate("DELETE FROM subscription WHERE number='"+row.getKey()+"'");		        
		        st.executeUpdate("INSERT INTO subscription values('"+row.getKey()+"','"+row.getValue()+"')");
		    }	    
			
		}catch(SQLException sqe){
			sqe.printStackTrace();
		}catch(Exception e){
			e.printStackTrace();
		}
  
	}
	
	

	private static void connect() throws Exception{   
		if(con==null){
			String url = "jdbc:mysql://mysql.abhardwaj.org/abhardwaj_default_db";
			BASE64Decoder decoder = new BASE64Decoder();
			
			try {
				String user = new String(decoder.decodeBuffer("X215c3FsX2FkbWlu"));
				String password = new String(decoder.decodeBuffer("SkNBVDA0ODY="));
				con = DriverManager.getConnection(url, user, password);
				st = con.createStatement();
			}catch (Exception e) {
				throw e;
			} 
		}
	    
	}

}
