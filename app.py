import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

cred = credentials.Certificate("private/chemsafe---argan-s-lab-firebase-adminsdk-fbsvc-10f6bd9f8c.json")
firebase_admin.initialize_app(cred)

app.secret_key = 'secret'

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get['email']
        password = request.form.get['password']
        
        try:
            # Create a new user in Firebase
            user = auth.create_user(email=email, password=password)
            flash('User created successfully!', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after signup
        except auth.EmailAlreadyExistsError:
            flash('Email already exists. Try logging in instead.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    
    return render_template('signup.html')


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = auth.get_user_by_email(email)
            flash(f'Successfully found user {email}', 'success')
            return redirect(url_for('welcome')) 
        except auth.UserNotFoundError:
            flash('No user found with that email.', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    
    return render_template('login.html')


# Route for welcome page after successful login
@app.route('/welcome')
def welcome():
    return 'Welcome to the app!'


table_data = []
# Route for dashboard page
@app.route('/dashboard')
def index():
    return render_template('dashboard.html', table_data=table_data)

@app.route('/add', methods=['POST'])
def add():
    cpdcode = request.form.get('cpdcode')
    chemical_structure = request.form.get('chemical_structure')
    yield_ = request.form.get('yield_')
    purity = request.form.get('purity')
    solubility = request.form.get('solubility')
    location = request.form.get('location')
    physical_appearance = request.form.get('physical_appearance')
    synthestic_protocol = request.form.get('synthestic_protocol')

    
    table_data.append({'cpdcode': cpdcode, 
                       'chemical_structure': chemical_structure, 
                       'yield_': yield_, 
                       'purity': purity, 
                       'solubility': solubility, 
                       'location': location,
                       'physical_appearance': physical_appearance,
                       'synthestic_protocol': synthestic_protocol})
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)