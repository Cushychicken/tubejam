from flask import Flask, render_template, request
from forms import YoutubeForm, RegisterForm
from models import db, Signup


class Settings:
    DB_NAME = "registrants.db"
    # Put the db file in project root
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_NAME)
    DEBUG = True
    SECRET_KEY = 'MONKEYFUCKER'

app = Flask(__name__)
app.config.from_object(Settings)

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

@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works!'
    else:
        return 'Somethings broke.'

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000)
