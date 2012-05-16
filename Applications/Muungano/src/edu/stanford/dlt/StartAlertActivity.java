package edu.stanford.dlt;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

public class StartAlertActivity extends Activity {
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	super.onCreate(savedInstanceState); 
    	showDialog(1);
                
        
    }
    
    @Override
    protected Dialog onCreateDialog(int id) {
	    AlertDialog.Builder builder = new AlertDialog.Builder(this);
	    switch(id){
	    case 1:
		    final CharSequence[] items = {"New Alert", "Cancel Alert"};	   
		    builder.setTitle("Pick an option");
		    builder.setItems(items, new DialogInterface.OnClickListener() {
		        public void onClick(DialogInterface dialog, int item) {
		        	if(item == 0){		        		
		            	Alert.send("ALERT 1");
		        		showDialog(2);
		        		dialog.dismiss();
		        	}else{
		        		//Alert.send("ALERT CANCEL");
		        		showDialog(3);
		        		dialog.dismiss();	        		
		        	}
		        }
		    });
		    break;
	    case 2:
		    builder.setMessage("Alert Initiated.")
		           .setCancelable(false)		          
		           .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
		               public void onClick(DialogInterface dialog, int id) {
		                    StartAlertActivity.this.finish();
		               }
		           });
		    break;
	    	case 3:
		    builder.setMessage("Alert Cancelled.")
		           .setCancelable(false)
		           .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
		               public void onClick(DialogInterface dialog, int id) {
		                    StartAlertActivity.this.finish();
		               }
		           });
		    break;
	    }
	    AlertDialog alert = builder.create();
	    return alert;
    }
    
   
	
}