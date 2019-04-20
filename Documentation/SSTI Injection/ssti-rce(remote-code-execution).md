## Flask Jinja 2 Remote Code Execution

Go to http://localhost:5000/ssti to view the render template vulnerable to remote code execution

Then Navigate to http://10.0.0.19:5000/ssti?name=drew<script>alert("hello");</script> for testing a simple remote code alert

Since our jinja page is does not have no-script enabled we are able to simply execute javascript in the field

With this in mind we can execute numerous Remote Code Executions to query the server for useful information!

