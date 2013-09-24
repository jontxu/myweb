from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from config import LANGUAGES
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config['DEBUG'] = True

babel = Babel(app)
assets = Environment(app)
assets.url = app.static_url_path

less = Bundle('stylesheets/main.less', 'stylesheets/sprites.less', filters='less, cssmin', output='stylesheets/style.min.css')
js = Bundle('javascripts/jquery.js', 'javascripts/html5shiv.js', filters='closure_js', output='javascripts/all.min.js')

assets.register('less', less)
assets.register('js', js)

@app.route('/')
def index():
	return render_template('index.html', title='Jon')

@app.route('/career/')
def career():
	return render_template('career.html', title='My career')

@app.route('/projects/')
def projects():
	return render_template('projects.html', title='Projects')

@app.route('/tech/')
def tech():
	return render_template('tech.html', title='Technologies')

@app.route('/contact/')
def contact():
	return render_template('contact.html', title='Contact')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
   app.run()