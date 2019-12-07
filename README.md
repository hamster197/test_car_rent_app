The system provides the work of the organization for the delivery of cars for rent.
The user can rent different cars and the car can be rented to different users.
The user has attributes email, name, language (en, ru). The machines have the attributes name (specified in two languages en, ru, implementation to make taking into account the possible increase in languages), the year of creation, and the date of adding the machine to the system.
RestAPI with the following functionality:
- registered user
- get user machines
- change user data
- get all users
For api authorization via token based authentication.
By RestApi, the machine name is given in the user's language.
The site provides the following functionality:
- register user/login
- add a machine into the system
- add the machine to the user
- information about the user
- change user information
Only the register user/login page is available to a non-authorized user, when other pages are opened by a non-authorized user, a redirect is made to the register user/login page.
When you add a machine, an email is sent to the user.
An email-password pair is used for authorization.
Test scenario.
Deploy the system through docker-compose.
