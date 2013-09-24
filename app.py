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
def hello_world():
	return render_template('test.html', title='Test')

@app.route('/about/')
def about():
	return render_template('test.html', title='About me')

@app.route('/tech/')
def tech():
	return render_template('test.html', title='Technologies')

@app.route('/contact/')
def contact():
	return render_template('test.html', title='Contact')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
   app.run()