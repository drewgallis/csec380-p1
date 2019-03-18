# Questions - Activity 1

- What is the URL of your Github project?

    *https://github.com/drewgallis/csec380-p1*
    
- How did you breakup your projects and what are the security ramifications?

    *We broke up our project into multiple segments to help us determine security controls that need to be set in place. Based on the services we will be utilizing a FLASK authentication server with a Traefik Load balancer to handle our Nginx Webservers. In order to securly allow user browsing we will be using SSL encryption and also security measures to ensure our database is secure with holding user data.*
    
- How did you choose to break down your Epic into various issues (tasks)?

    *Our epic will be broken down into the implementation of various services, user experiences. To classify this easier we will most likely break down each epic into a service implementation such as etablishing an authentication server w/ backend code or creating a load balancing server w/ config.*
    
- How long did you assign each sprint to be?

    *2 weeks*
    
- Did you deviate from the Agile methodology at all? If yes, what is your reasoning for this?

    *During this project I hope to utilize as many agile methodoligies as we can with a high stress on (top-down) vetical developement (creating services with functionallity rather than trying to do them all at once.*
    
- How do you ensure that after each issue/milestone that security has been verified? How would you identify such issues in an ideal environment?

    *After each milestone we will run web automation tests to help us better understand potential security issues/vulnerablities. Also we may take the time to implement a headless web scanner (OWASP ZAP) to help us better understand possible vulnerabilites in our implementation.*
