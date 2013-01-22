var express = require('express');
var app = express();

app.get('/', function(req, res){
  	console.log(req.params);
	res.send('hello voicex');
});

app.get('/voicex_us', function(req, res){
  	console.log(req.params);
	res.send('ok');
});

app.get('/voicex_ke', function(req, res){
  	console.log(req.params);
	res.send('ok');
});


app.listen(8000);
console.log('server started on port 8000');
