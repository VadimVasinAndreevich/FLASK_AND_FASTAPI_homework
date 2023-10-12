"""
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
"""

from flask import Flask, request, render_template, redirect, url_for, session, flash
from homework_3.models import db, User
from flask_wtf.csrf import CSRFProtect
from homework_3.forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'bdfd4abee1bdec8a459c7e50f8c97dea1300aab823dfcb366265013a62e149eb'
app.config['SECRET_KEY'] = 'e511faf185d536df046464f80dc645d0c8166ca25f5c634eaf4b89c6ba344142'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
csrf = CSRFProtect(app)


@app.route('/')
def html_index():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.all()
        for el in range(len(user)):
            test_str = str(user[el]).split(',')
            if email == test_str[1] and check_password_hash(test_str[2], password):
                session['name'] = test_str[0]
                return render_template('exit.html', form=form)
        session['message'] = 'Учётная запись не существует, проверьте почту и пароль, или зарегистрируйтесь'
        return render_template('login.html', form=form)
    session.pop('message', None)
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        try:
            name = form.name.data
            surname = form.surname.data
            email = form.email.data
            password = form.password.data
            user = User(name=f'{name}', surname=f'{surname}', email=f'{email}',
                        password=f'{generate_password_hash(password)}')
            db.session.add(user)
            db.session.commit()
            session['mess'] = 'Регистрация прошла успешно!'
            return render_template('register.html', form=form)
        except:
            session['mess_one'] = 'Учётная запись уже существует'
            return render_template('register.html', form=form)
    session.pop('mess', None)
    session.pop('mess_one', None)
    return render_template('register.html', form=form)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("del-com")
def del_user():
    user = User.query.filter_by(name='Вадим').first()
    db.session.delete(user)
    db.session.commit()


@app.route('/index/')
def index():
    flash('Форма успешно отправлена!', 'success')
    return render_template('exit.html')


@app.route('/candy/')
def candy():
    context = {'title': 'Леденцы'}
    return render_template('candy.html', **context)


@app.route('/ice_cream/')
def ice_cream():
    context = {'title': 'Мороженное'}
    return render_template('ice_cream.html', **context)


@app.route('/cake/')
def cake():
    context = {'title': 'Тортики'}
    return render_template('cake.html', **context)


@app.route('/name/')
def name():
    persones = [{'name': 'Никита',
               'patronymic': 'Антонович',
               'surname': 'Шоколадов',
               'position': 'Директор',
               'mail': 'nik@mail.ru',
               'phone': '+7-987-654-32-10',
               },
              {'name': 'Анна',
               'patronymic': 'Антоновна',
               'surname': 'Тортикова',
               'position': 'Зам.Директора',
               'mail': 'Anna@mail.ru',
               'phone': '+7-932-667-31-12',
               },
              {'name': 'Елена',
               'patronymic': 'Константиновна',
               'surname': 'Конфетова',
               'position': 'Бухгалтер',
               'mail': 'Elena@mail.ru',
               'phone': '+7-913-752-28-23',
               }, ]
    context = {'persones': persones}
    return render_template('tab.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
