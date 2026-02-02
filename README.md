# URL Shortener

A simple Django-based URL shortener with user authentication.

## Features

- User signup and login
- Create, edit, and delete short URLs
- Track click counts
- Prevent duplicate short URLs per user
- Simple Bootstrap-based UI

### Installation

1. Clone the repository:
      git clone https://github.com/Irfan-Alaam/url_shortener.git

2. Create a virtual environment and activate it:

      To create: python -m venv .env
      To activate:
        Windows: .env\Scripts\activate
        Mac: source .env/bin/activate

3. Install dependencies:

      pip install -r requirements.txt

4. Run the server:

      python manage.py runserver

5. Open the app in your browser:

      http://127.0.0.1:8000/

##Requirements achieved:
      1. User can signup using unique username and strong password, if not matched with the error is raised<br>
      2. User can login only using valid credentails<br>
      3. Only loggedin users can create short URLs<br>
      4. Authenticated users can input a long URL (starting with https://) and receive a unique short key<br>
      5. Each generated short URL is unique<br>
      6. Constraints prevent creating a short URL for a long URL that is already shortened for the same user<br>
      7. Success and error messages are displayed for all actions (create, edit, login, signup)<br>
      8. Each short URL tracks the number of times it has been clicked
