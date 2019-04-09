## Blind Sql Injection Tutorial

Go to http://localhost:5000/sql_add_tmp to add a user to the tmp table for testing

Then Navigate to http://10.0.0.19:5000/sql_blind for testing a classic injection attack

Since our sql statement is: ['SELECT * FROM tmpUser WHERE `username` ="' + username + '" AND `password` ="' + password + '"']

We can use that to our advantage by inserting an injection statement like `" or ""="` into the username and password fields in the login page

Then based on that the database should dump the current credentials you just added! 

But since this is blind sql injection, if you enter a command that does not work, you will not get an error output.