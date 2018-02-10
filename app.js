var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var fs = require('fs');

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();
var router = express.Router();
var formidable = require('formidable');
var azure = require('azure-storage');

name = "rawmathpics";
key = "bMbE1GoaW/YWZghXo7i+y/HBlqFdVuIgK35gm5LMB1OxCmokkhoQ2CFkIrlVDOxwjmnLdNA2NOWVtHo82WZ7JQ==";
var blobSvc = azure.createBlobService(name, key);

var spawn = require('child_process').spawn;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', index);
app.use('/users', users);

router.post('/image', function (req, res) {
  var form = new formidable.IncomingForm();
  form.parse(req, function (err, fields, files) {
    var oldpath = files.pic.path;
    var newpath = __dirname + '/target.png';

    console.log(oldpath);
    fs.rename(oldpath, newpath, function () {
      var process = spawn('python', [__dirname + '/THacks18/main.py']);
      process.stdout.on('data', function (data){
        var obj = new Object();
        obj.latex = data;
        res.render('result', obj);
      });
    })

    /*blobSvc.createBlockBlobFromLocalFile('pics', name.toString(), oldpath, function (error, result, response) {
      if (!error) {
        var process = spawn('python', [__dirname + '/test.py', oldpath]);
        process.stdout.on('data', function (data){
          res.write(data);
          res.end();
        });
      }
    });*/
    //res.send("{'text':'File uploaded and move\n'");
  });
});

router.post('/image2', function (req, res) {
  var form = new formidable.IncomingForm();
  form.parse(req, function (err, fields, files) {
    var oldpath = files.pic.path;
    var newpath = __dirname + '/target.png';
    var obj = new Object();
    obj.latex = "X^{2}+5n+2";

    res.render('result', );

  });
});
app.use('/process', router);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
 // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
