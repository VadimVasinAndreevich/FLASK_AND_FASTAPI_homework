"""
Создать базовый шаблон для интернет-магазина,
содержащий общие элементы дизайна (шапка, меню, подвал),
и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def html_index():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


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
