# Questions - Activity 3

- Provide a link to the test cases you generated for this activity.
	
- How do you ensure that users that navigate to the protected pages cannot bypass authentication requirements?
	
- How do you protect against session fixation?
	To prevent this our web app will supply a different sessionID cookie after the user has successfully authenticated into our site.
- How do you ensure that if your database gets stolen passwords aren’t exposed?
	We can ensure that they will not get exposed because we never save our passwords in plaintext. We only have the hashes and use a secure hash algorithm.
- How do you prevent password brute force?
	We will only allow a user to try their password 3 times before preventing them for further attempts and providing them a way to reset their password.
- How do you prevent username enumeration?
	When a user inputs the wrong username or password, we will not tell them which field had a correct value therefore preventing an attacker from enumerating usernames.
- What happens if your sessionID is predictable, how do you prevent that?
	If our sessionID is predictable than an attacker can strategically guess the value to bypass our authentication. To prevent this we generate a random value for the sessionID that way it is not guessable.