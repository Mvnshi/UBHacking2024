# app.py
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from flask_session import Session

# Initialize Flask and session
app = Flask(__name__)
app.secret_key = 'abcdefg123789000000'
app.config.from_object('config')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize Auth0 OAuth client
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=app.config['DISCOVERY_URL'],
    # Only add the audience parameter if AUTH0_AUDIENCE is not None
    authorize_params={'audience': app.config['AUTH0_AUDIENCE']} if app.config['AUTH0_AUDIENCE'] else {}
)

# Routes
@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=app.config['AUTH0_CALLBACK_URL'])

@app.route('/callback')
def callback_handling():
    # Handle the callback from Auth0 and retrieve access token
    auth0.authorize_access_token()

    # Use the full URL for the userinfo endpoint
    user_info = auth0.get(f'https://{app.config["AUTH0_DOMAIN"]}/userinfo').json()

    # Store user information in the session
    session['user'] = user_info
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f'https://{app.config["AUTH0_DOMAIN"]}/v2/logout?returnTo={url_for("home", _external=True)}&client_id={app.config["AUTH0_CLIENT_ID"]}'
    )

@app.route('/take-note')
def take_note():
    return render_template('newnotes.html')

@app.route('/view-note')
def view_note():
    return render_template('view-notes.html')

@app.route('/mind-map')
def mind_map():
    return render_template('graph.html')

@app.route('/time-management')
def time_management():
    return render_template('Time.html')

@app.route('/syllabus-scanner')
def syllabus_scanner():
    return render_template('sylabus.html')

if __name__ == '__main__':
    app.run(debug=True)
