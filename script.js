var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Shaigal5%",
  database: "testdb"
});

con.connect(function(err) {
  if (err) throw err;
  	con.query("SELECT ItemName FROM item_info", function (err, result, fields) {
  if (err) throw err;
  	console.log(result);
  });
});

