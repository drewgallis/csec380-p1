# Questions - Activity 2

- What Web Application security mechanisms are involved in your topology? What security mechanisms would ideally be involved?
    *Currently our web application is implementing a FLASK authetnication framework, allowing users with valid credientals to login. Also, we plan on integrating a docker headless zedd attack proxy to help us better understand what parts of our web related services are vulnerable.
- What testing framework did you choose and why?
    For our testing framework we chose to implement python requests and beatuiful soup for parsing html input. We chose beautiful soup because it is extremely simple and easy to scrape in python. Overall, beautiful soup may be changed into selenium for more automation controls in the future.
