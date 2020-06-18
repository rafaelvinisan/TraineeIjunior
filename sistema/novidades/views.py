from flask import Blueprint, render_template, request, redirect, url_for
from sistema import db
from sistema.novidades.models import Novidade
from datetime import datetime

novidades = Blueprint('novidades', __name__, template_folder="templates")


@novidades.route('/')
def index():
    novidades = Novidade.query.order_by(Novidade.id.desc()).all()
    return render_template('novidades.html', novidades_front=novidades)


@novidades.route('/adicionar-novidade/', methods=['GET', 'POST'])
def adicionar_novidade():
    if request.method == 'POST':
        titulo = request.form['title']
        mensagem = request.form['mensagem']
        nome = request.form['nome']

        novidade = Novidade(titulo, mensagem, nome)
        db.session.add(novidade)
        datenow = datetime.utcnow()
        novidade.pub_date = datenow.strftime("%x")
        # split_date = novidade.pub_date.split(" ", 1)
        # novidade.pub_date = split_date[0].replace('-', '/')

        db.session.commit()
        return redirect(url_for('novidades.index'))

    return render_template('adicionar-novidade.html')
