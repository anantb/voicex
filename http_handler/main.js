var express = require('express');
var app = express();

app.get('/', function(req, res){
  res.send('hello voicex');
});

app.listen(3000);
