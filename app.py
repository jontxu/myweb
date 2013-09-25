from flask import Flask, render_template, request, flash
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from flask_wtf.csrf import CsrfProtect
from config import LANGUAGES
from werkzeug.contrib.fixers import ProxyFix
from contact import ContactForm
from flask.ext.mail import Message, Mail
 
mail = Mail()

csrf = CsrfProtect()
app = Flask(__name__)

app.config['DEBUG'] = True
app.secret_key = 'thisisakey'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'jonjc22@gmail.com'
app.config["MAIL_PASSWORD"] = 'pass'

mail.init_app(app)

csrf.init_app(app)
babel = Babel(app)
assets = Environment(app)
assets.url = app.static_url_path

less = Bundle('stylesheets/main.less', 'stylesheets/sprites.less', filters='less, cssmin', output='stylesheets/style.min.css')
js = Bundle('javascripts/jquery.js', 'javascripts/html5shiv.js', filters='closure_js', output='javascripts/all.min.js')

assets.register('less', less)
assets.register('js', js)

@csrf.error_handler
def csrf_error(reason):
	return render_template('error.html', error=reason)

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

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender=form.email.data, recipients=app.config["MAIL_USERNAME"] )
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', title='Contact', success=True)
  elif request.method == 'GET':
    return render_template('contact.html', title='Contact', form=form)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
   app.run()