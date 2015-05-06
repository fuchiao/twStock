var express = require('express')
var bodyParser = require('body-parser');
var multer = require('multer');
var app = express();

var fs = require('fs');
var sql = require('sqlite3').verbose();
var csv = require('csv');
app.use(bodyParser.json()); // for parsing application/json  
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded  
app.use(multer()); // for parsing multipart/form-data  

app.get('/', function(req, res) {
    res.sendFile(__dirname+'/index.html');
    console.log("visit home");
});
app.get('/TWII', function(req, res) {
    csv.parse(fs.readFileSync('./TWII.csv'), function(err, data) {
        var headers = data[0];
        data.shift();
        var result = [];
        for (var i = 0; i < data.length; i++) {
            result.push({});
            for (var j = 0; j < headers.length; j++) {
                result[result.length-1][headers[j]] = data[i][j];
            }
        }
        res.send(result);
    });
    console.log("visit TWII.csv");
});
app.get('/0050', function(req, res) {
    csv.parse(fs.readFileSync('./0050.csv'), function(err, data) {
        var headers = data[0];
        data.shift();
        var result = [];
        for (var i = 0; i < data.length; i++) {
            result.push({});
            for (var j = 0; j < headers.length; j++) {
                result[result.length-1][headers[j]] = data[i][j];
            }
        }
        res.send(result);
    });
    console.log("visit 0050.csv");
});
var server = app.listen(1337, function () {
    var host = server.address().address
    var port = server.address().port
    console.log('Example app listening at http://%s:%s', host, port)
})



