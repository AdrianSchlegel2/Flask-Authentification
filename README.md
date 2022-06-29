# Flask Authentification

I used the **Python Webframework Flask** to create a website that is a login/register website with a "secret" for people who create an account. 
I used **SQLAlchemy Databases** to store the data of the users and to protect the passwords from potential hackers I used the **werkzeug web application library** to hash as well as salt the passwords. I also used the **Flask-login library** to manage users on this website. I also implemented decorator functions like the @login_required to inhibit users that have not logged in to enter certain parts of the website and the **send_from_directory** to allow the user to download a file from my website 
