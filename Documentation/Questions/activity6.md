# Questions - Activity 6

- How would you fix your code so that this issue is no longer present?

*It is prevented buy the Same Origin Policy as well as our CSRF tokens in that a person with an invalid session cannot mess with another users valid session.*

- How does your test demonstrate SSRF as opposed to just accessing any old endpoint?

*Our test utilizes a script exploit in Jinja2 that allows a user to query the server for internal files and execute code.*