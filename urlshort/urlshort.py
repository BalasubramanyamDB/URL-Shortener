from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json 
import os
from werkzeug.utils import secure_filename

# app = Flask(__name__)

# app.secret_key = 'jb23jb4235b2i5kb235b2h3j6b21gj41f2yh1'

bp = Blueprint('urlshort',__name__)
@bp.route('/')
def home():
    return render_template('home.html', codes = session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as file:
                urls = json.load(file)

            if request.form['code'] in urls.keys():
                flash('Shorten name already taken')
                return redirect(url_for('urlshort.home'))  
             
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}

        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('urlshort/static/user_files/'+full_name)
            urls[request.form['code']] = {'file':full_name}


        with open('urls.json', 'w') as file:
            json.dump(urls, file, indent=4)
        session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home')) 
    

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as file:
            urls = json.load(file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/'+urls[code]['file']))

    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))