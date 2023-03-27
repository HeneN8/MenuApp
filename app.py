from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

# define a list of available menus
menus = [
    {'name': 'Menu 1', 'description': 'This is menu 1'},
    {'name': 'Menu 2', 'description': 'This is menu 2'},
    {'name': 'Menu 3', 'description': 'This is menu 3'},
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are correct
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Redirect to the home page
            return redirect('/home')
        else:
            # Show an error message
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')

# define a route for the homepage
@app.route('/home')
def home():
    # render the homepage template with the available menus and the user's current selections
    return render_template('home.html', menus=menus, user_menus=user_menus)


# define a list to keep track of user menu selections
user_menus = []

# define a route for the menu sign-up page
@app.route('/signup', methods=['POST'])
def signup():
    # get the selected menu from the form data
    selected_menu = request.form['menu']
    # add the selected menu to the user's menu selections in the database
    user = User.query.filter_by(username=session["username"]).first()
    user_menu = UserMenu(user_id=user.id, menu_name=selected_menu)
    db.session.add(user_menu)
    db.session.commit()
    # redirect the user back to the homepage
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()

