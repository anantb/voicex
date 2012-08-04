package edu.stanford.dlt;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.widget.TextView;

public class ImmediateAlertActivity extends Activity {
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	TextView t = new TextView(this.getApplicationContext());
        super.onCreate(savedInstanceState); 
        Alert.send("ALERT");        
        showDialog(0);
    }
    
    @Override
    protected Dialog onCreateDialog(int id) {
	    AlertDialog.Builder builder = new AlertDialog.Builder(this);	    
	    builder.setMessage("Alert Sent.")
	           .setCancelable(false)		          
	           .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
	               public void onClick(DialogInterface dialog, int id) {
	                    ImmediateAlertActivity.this.finish();
	               }
	           });
		   
	    	
	    AlertDialog alert = builder.create();
	    return alert;
    }
    
   
	
}