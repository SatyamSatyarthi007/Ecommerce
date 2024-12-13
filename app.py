from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)

# Add these session configurations
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',  # or 'None' if you need cross-site access
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)  # Session expires after 30 minutes
)

# Initialize MySQL
mysql = MySQL(app)

@app.before_request
def make_session_permanent():
    session.permanent = True  # Set session to use PERMANENT_SESSION_LIFETIME

@app.route('/')
def home():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form.get('login-email')
        password = request.form.get('login-password')

        if not email or not password:
            flash("Please fill in all fields", "danger")
            return redirect(url_for('login'))

        try:
            cur = mysql.connection.cursor()
            
            # First, let's check the user's data including gender
            cur.execute("SELECT id, name, email, password, gender FROM users WHERE email = %s AND password = %s", 
                       (email, password))
            user = cur.fetchone()
            
            # Debug prints
            print("Full user data:", user)
            
            if user:
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                user_gender = user[4]  # Get gender from the query result
                
                print(f"User ID: {user[0]}")
                print(f"User Name: {user[1]}")
                print(f"User Gender: {user_gender}")
                
                flash("Login successful!", "success")
                
                # Explicit gender check
                if user_gender and user_gender.lower().strip() == 'male':
                    print("Redirecting to male shop")
                    return redirect(url_for('shopmale'))
                else:
                    print("Redirecting to female shop")
                    return redirect(url_for('shopfemale'))
            else:
                flash("Invalid email or password", "danger")
                
            cur.close()
        
        except Exception as e:
            flash("An error occurred during login", "danger")
            print(f"Login error: {str(e)}")

        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['signup-name']
        email = request.form['signup-email']
        password = request.form.get('signup-password')
        gender = request.form.get('signup-gender')
        
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password, gender) VALUES (%s, %s, %s, %s)",
                (name, email, password, gender)
            )
            mysql.connection.commit()
            cur.close()
            
            flash("Signup successful!", "success")
            
            if gender == 'male':
                return redirect(url_for('shopmale'))
            elif gender == 'female':
                return redirect(url_for('shopfemale'))
            
        except Exception as e:
            flash("An error occurred during signup", "danger")
            print(f"Signup error: {str(e)}")
            return redirect(url_for('signup'))
    
    return render_template('login.html')

@app.route('/shop')
def shop():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT gender FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        
        if user and user[0] == 'male':
            return redirect(url_for('shopmale'))
        else:
            return redirect(url_for('shopfemale'))
    return render_template('shop.html')

@app.route('/shopmale')
def shopmale():
    return render_template('shopmale.html')

@app.route('/shopfemale')
def shopfemale():
    return render_template('shopfemale.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/cart')
def cart():
    return render_template('cart.html')
    

# Add this new route to app.py
@app.route('/debug/users')
def debug_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, created_at FROM users")  # Excluding password for security
        users = cur.fetchall()
        cur.close()
        
        # Format the data for display
        users_list = []
        for user in users:
            users_list.append({
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'created_at': user[3]
            })
        
        return {'users': users_list}
    except Exception as e:
        return {'error': str(e)}

# For development only - remove in production
if app.debug:
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        REMEMBER_COOKIE_SECURE=False
    )

@app.route('/debug/session')
def debug_session():
    return {
        'session': dict(session),
        'authenticated': 'user_id' in session
    }

@app.route('/debug/db')
def debug_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        
        table_structure = None
        if ('users',) in tables:
            cur.execute("DESCRIBE users")
            table_structure = cur.fetchall()
        
        cur.close()
        
        return {
            'connection': 'success' if result else 'failed',
            'tables': [table[0] for table in tables],
            'users_table_structure': table_structure
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        
        if result:
            return {
                'status': 'success',
                'message': 'Database connection successful',
                'result': result
            }
        else:
            return {
                'status': 'error',
                'message': 'No result returned'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == '__main__':
    app.run(debug=True)
