# -*- coding: utf-8 -*-

import os
import config
from flask import Flask, render_template, request, flash
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel
from flask_wtf.csrf import CsrfProtect
from werkzeug.contrib.fixers import ProxyFix
from contact import ContactForm
from flask.ext.mail import Message, Mail
from flask_sslify import SSLify

mail = Mail()
csrf = CsrfProtect()
app = Flask(__name__)
#sslify = SSLify(app)

app.secret_key = 'thisisakey'

if os.environ.get('HEROKU') is None:
  app.config.from_object('config.Development')
  print 0
else:
  app.config.from_object('config.Production')
  print 1

mail.init_app(app)
csrf.init_app(app)
assets = Environment(app)
assets.config['less_run_in_debug'] = False
assets.url = app.static_url_path

less = Bundle('stylesheets/main.less', 'stylesheets/img.less', filters='less,cssmin', output='stylesheets/style.min.css', extra={'rel': 'stylesheet/less' if assets.debug else 'stylesheet'})
js = Bundle('javascripts/jquery.js', 'javascripts/html5shiv.js', 'http://lesscss.googlecode.com/files/less-1.3.0.min.js', filters='closure_js', output='javascripts/all.min.js')

assets.register('less', less)
assets.register('js', js)

@csrf.error_handler
def csrf_error(reason):
	return render_template('error.html', error=reason)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.static_url_path), 'ico/favicon.ico')

@app.route('/')
def index():
	return render_template('index.html', title='Jon')

@app.route('/resume/')
def resume():
	return render_template('resume.html', title=u'R\xe9sum\xe9')

@app.route('/projects/')
def projects():
	return render_template('projects.html', title='Projects')

@app.route('/tech/')
def tech():
	return render_template('tech2.html', title='Technologies')

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
   port = int(os.environ.get("PORT", 5000))
   app.run()
