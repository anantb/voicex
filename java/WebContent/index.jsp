<!doctype html>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="sun.misc.BASE64Decoder, edu.stanford.voicex.*"%>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>DLT Prototype</title>
        <link rel="stylesheet" href="themes/css/apple.css" title="dlt">

        <script src="src/lib/zepto.min.js" type="text/javascript" charset="utf-8"></script>
        <script src="src/jqtouch.min.js" type="text/javascript" charset="utf-8"></script>
        <!-- Uncomment the following two lines (and comment out the previous two) to use jQuery instead of Zepto. -->
        <!-- <script src="../../src/lib/jquery-1.7.min.js" type="application/x-javascript" charset="utf-8"></script> -->
        <!-- <script src="../../src/jqtouch-jquery.min.js" type="application/x-javascript" charset="utf-8"></script> -->

        <script src="extensions/jqt.themeswitcher.min.js" type="application/x-javascript" charset="utf-8"></script>

        <script type="text/javascript" charset="utf-8">
            var jQT = new $.jQTouch({
                icon: 'jqtouch.png',
                icon4: 'jqtouch4.png',
                addGlossToIcon: false,
                startupScreen: 'jqt_startup.png',
                statusBar: 'black-translucent',
                themeSelectionSelector: '#jqt #themes ul',
                preloadImages: []
            });

            // Some sample Javascript functions:
            $(function(){

                // Show a swipe event on swipe test
                $('#swipeme').swipe(function(evt, data) {
                    var details = !data ? '': '<strong>' + data.direction + '/' + data.deltaX +':' + data.deltaY + '</strong>!';
                    $(this).html('You swiped ' + details );
                    $(this).parent().after('<li>swiped!</li>')
                });

                $('#tapme').tap(function(){
                    $(this).parent().after('<li>tapped!</li>')
                });

                $('a[target="_blank"]').bind('click', function() {
                    if (confirm('This link opens in a new window.')) {
                        return true;
                    } else {
                        return false;
                    }
                });

                // Page animation callback events
                $('#pageevents').
                    bind('pageAnimationStart', function(e, info){ 
                        $(this).find('.info').append('Started animating ' + info.direction + '&hellip;  And the link ' +
                            'had this custom data: ' + $(this).data('referrer').data('custom') + '<br>');
                    }).
                    bind('pageAnimationEnd', function(e, info){
                        $(this).find('.info').append('Finished animating ' + info.direction + '.<br><br>');

                    });
                
                // Page animations end with AJAX callback event, example 1 (load remote HTML only first time)
                $('#callback').bind('pageAnimationEnd', function(e, info){
                    // Make sure the data hasn't already been loaded (we'll set 'loaded' to true a couple lines further down)
                    if (!$(this).data('loaded')) {
                        // Append a placeholder in case the remote HTML takes its sweet time making it back
                        // Then, overwrite the "Loading" placeholder text with the remote HTML
                        $(this).append($('<div>Loading</div>').load('ajax.html .info', function() {        
                            // Set the 'loaded' var to true so we know not to reload
                            // the HTML next time the #callback div animation ends
                            $(this).parent().data('loaded', true);  
                        }));
                    }
                });
                // Orientation callback event
                $('#jqt').bind('turn', function(e, data){
                    $('#orient').html('Orientation: ' + data.orientation);
                });
                
            });
        </script>
        <style type="text/css" media="screen">
            #jqt.fullscreen #home .info {
                display: none;
            }
            div#jqt #about {
                padding: 100px 10px 40px;
                text-shadow: rgba(0, 0, 0, 0.3) 0px -1px 0;
                color: #999;
                font-size: 13px;
                text-align: center;
                background: #161618;
            }
            div#jqt #about p {
                margin-bottom: 8px;
            }
            div#jqt #about a {
                color: #fff;
                font-weight: bold;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        
            <div id="home" class="current">
                <div class="toolbar">
                    <h1>Muungano</h1>
                    <a class="button slideup" id="about" href="#">About</a>
                </div>
                <div class="scroll">
                    <ul class="rounded">
                        <li class="arrow"><a href="#send_immediate">Send Immediate Alert</a> </li>
                        <li class="arrow"><a href="#send_delayed">Schedule an Alert</a></li>
                        <li class="arrow"><a href="#cancel">Cancel the Scheduled Alert</a></li>                        
                    </ul>                    
                </div>      
                
            </div>
            
            
            <div id="send_immediate">
                <div class="toolbar">
                    <h1>Muungano</h1>
                    <a class="button slideup" id="about" href="#">About</a>
                </div>
                <div class="scroll">
                <%
                
					
					
					try{
						String DEFAULT_USER = "aGVsbG9hbmFudDAwN0BnbWFpbC5jb20=";
						String DEFAULT_PASSWORD = "SkNhdDI1MDQ4Ng==";	
						String ALERT_NUMBER = "6503089145";
						VoiceX voicex;
						
						Config v_config = new Config();
						BASE64Decoder decoder = new BASE64Decoder();
						String user = new String(decoder.decodeBuffer(DEFAULT_USER));
						String password = new String(decoder.decodeBuffer(DEFAULT_PASSWORD));
						v_config.setProperty("user", user);
						v_config.setProperty("password", password);
						v_config.setProperty("loglevel", Integer.toString(Debug.TERSE));			 		
						Login login = new Login(v_config);
						voicex = new VoiceX(login);
						voicex.sendSMS(ALERT_NUMBER, "ALERT");	
						
					}catch(Exception e){
						e.printStackTrace();
					}
					

	
				       

                %> 
                Done.                     
                </div>      
                
            </div>
            
            
        
    </body>
</html>
