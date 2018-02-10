var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();
var router = express.Router();
var formidable = require('formidable');
var azure = require('azure-storage');

//var blobSvc = azure.createBlobService();

var spawn = require('child_process').spawn;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

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
    var newpath = __dirname + '/' + files.pic.name;
    console.log(newpath);
    console.log(oldpath);
    //fs.rename(oldpath, newpath, function(err){
      //if (err) throw err;
      var process = spawn('python', [__dirname + '/test.py']);
      process.stdout.on('data', function (data){
        res.write(data);
        res.end();
      });
      res.write('File uploaded and move\n');
    //});
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
