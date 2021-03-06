from flask import Flask, render_template, request
from forms import YoutubeForm, RegisterForm
from models import db, Signup
import youtube_dl as yt
import re

### YoutubeDL regex and setup ###

# Regex to find output file by its name
yt_re = re.compile(r'www\.youtube\.com/watch\?v=(\S+)')

# YoutubeDL options
#   -output format string
#   -extract only audio (i think)
ytdl_opts = { 'outtmpl': '%(id)s.%(ext)s',
              'extract-audio': True
            }
ytdl = yt.YoutubeDL(ytdl_opts)

# Set default info to extract
ytdl.add_default_info_extractors()


class Settings:
    DB_NAME = "registrants.db"
    # Put the db file in project root
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_NAME)
    DEBUG = True
    SECRET_KEY = 'MONKEYFUCKER'

app = Flask(__name__)
app.config.from_object(Settings)

@app.route('/', methods=['GET','POST'])
def main():
    form = YoutubeForm()
    if request.method == 'POST' and form.validate():
        youtube_url = form.url.data
        result = yt_re.search(youtube_url)
        if result:
            video = ytdl.extract_info(youtube_url, download=True)
            return result.group(1) + ' ' + youtube_url
        else:
            return youtube_url
    elif request.method == 'GET':
        return render_template('main.html', form=form)

# Registration Page (let people be posted)
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        teststr = form.email.data.lower()
        email_test = Signup.query.filter_by(email=teststr).first()
        if email_test:
            return "That email is taken!"
        else:
            newuser = Signup(name=form.name.data, email=form.email.data)
            db.session.add(newuser)
            db.session.commit()
            return render_template('thanks.html')
    elif request.method == 'GET':
        return render_template('register.html', form=form)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000)
