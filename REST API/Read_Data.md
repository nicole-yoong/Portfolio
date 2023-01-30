# Read data from Microsoft SQL Server in web browser #

### Install node from https://nodejs.org/en ###

### Create a directory ### 
mkdir SQLAPI
cd SQLAPI

### Initiate the node environment and install packages ###
npm init

npm install --save express
npm install --save mssql
npm install  --save msnodesqlv8
npm install --save json-beautify

### Create config.js ###
var config = {
  production: {
     driver: 'msnodesqlv8',
     connectionString: 'Driver=SQL Server Native Client 11.0;Server=LAPTOP-V0AH6EGV\\SQLEXPRESS;Database=Bathworld;Trusted_Connection=yes'
     } 
};
module.exports = config;

### Create ReadApp.js ###
// Read functions
const express = require('express'); 
const app = express();
const sql = require('mssql/msnodesqlv8') //mssql with MS driver for SQL Server
var beautify = require("json-beautify");
  
var env = process.env.NODE_ENV || 'production';
var sqlConfig = require('./config')[env];
  
// Start server and listen on http://localhost:2908/
var server = app.listen(2908, function() {
  var host = server.address().address
  var port = server.address().port
  
  console.log("app listening at http://%s:%s", host, port)
});
  
const connection = new sql.ConnectionPool(sqlConfig, function(err){
      if (err){
      console.log(err);
      }
    }
)
  
// Input as Integer
app.get('/emp/emp_id/:empid/', function(req, res) {
  connection.connect().then(pool => { 
    var conn=pool.request()
    var forInteger = /\b\d+\b/i; 
    if (forInteger.test(req.params.empID)) {  
       conn.input('input_parameter', sql.Int, req.params.empID)}
    else {conn.input('input_parameter', sql.Int, 32116)} 
    var string = 'SELECT * FROM dbo.emp WHERE emp_id  = @input_parameter'
    return conn.query(string)
  }).then(result => {
    let rows = result.recordset
    res.setHeader('Access-Control-Allow-Origin', '*')
      // Result to URL
   res.status(200).type('JSON').send(beautify(rows, null, 2, 100));
         
      // result to log
      console.log(beautify(rows, null, 2, 100));
    connection.close();
  }).catch(err => {
    console.log(err);
    res.status(500).send({
      message: err
    })
    connection.close();
  });
});
 
 
 // input as VarChar
 app.get('/emp/emp_title/:emptitle/', function(req, res) {
  connection.connect().then(pool => { 
    var conn=pool.request()
    conn.input('input_parameter', sql.VarChar, req.params.SamAccountName)
    var string = 'SELECT * FROM dbo.emp WHERE  emp_name = @input_parameter'
    return conn.query(string)
  }).then(result => {
    let rows = result.recordset
    res.setHeader('Access-Control-Allow-Origin', '*')
     
    res.status(200).type('JSON').send(beautify(rows, null, 2, 100));
         
    // result to log
    console.log(beautify(rows, null, 2, 100));
    connection.close();
  }).catch(err => {
    console.log(err);
    res.status(500).send({
      message: err
    })
    connection.close();
  });
});

node ReadApp.js
