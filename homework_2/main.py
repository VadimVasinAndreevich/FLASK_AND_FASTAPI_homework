"""
Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя,
а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти»,
при нажатии на которую будет удалён cookie-файл с данными пользователя и произведено перенаправление
на страницу ввода имени и электронной почты.
"""

from flask import Flask, request, render_template, make_response,\
    redirect, url_for, make_response, session, flash


app = Flask(__name__)
app.secret_key = 'bdfd4abee1bdec8a459c7e50f8c97dea1300aab823dfcb366265013a62e149eb'


@app.route('/')
def html_index():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


@app.route('/index/')
def index():
    if 'name' and 'email' in session:
        flash('Форма успешно отправлена!', 'success')
        return render_template('exit.html')
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('login'))
        if not request.form['email']:
            flash('Введите адрес электронной почты!', 'danger')
            return redirect(url_for('login'))
        if '@' not in request.form['email'] or \
                request.form['email'][-3:] != '.ru' and request.form['email'][-4:] != '.com':
            flash('Неверный адрес электронной почты!')
            flash('проверьте наличие символа "@" и доменов ".ru" или ".com"', 'danger')
            return redirect(url_for('login'))
        return redirect(url_for('index'))
    return render_template('contact.html')


@app.route('/logout/')
def logout():
    session.pop('name', None)
    session.pop('email', None)
    return render_template('contact.html')


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


if __name__ == "__main__":
    app.run(debug=True)
