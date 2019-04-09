## Classic Sql Injection Tutorial

Go to http://localhost:5000/sql_add_tmp to add a user to the tmp table for testing

Then Navigate to http://10.0.0.19:5000/sql_classic for testing a classic injection attack

Since our sql statement is: ['SELECT * FROM tmpUser WHERE `username` ="' + username + '" AND `password` ="' + password + '"']

We can use that to our advantage by inserting `" or ""="` into the username and password fields in the login page

Then based on that the database should dump the current credentials you just added!

