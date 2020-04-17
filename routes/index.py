from flask import (
    Blueprint,
    redirect,
    abort,
    session,
    render_template,
    request,
    url_for,
)
from models.user import User
from utils import log
from . import current_user

main = Blueprint('index', __name__)


@main.route('/')
def index():
    message = ''
    return render_template('index.html', message=message)


@main.route('/login', methods=['POST'])
def login():
    u = User.validate_login(request.form)
    if u is None:
        message = '* 账号或密码错误'
        return render_template('index.html', message=message)
    session['user_id'] = u.id
    session.permanent = True
    return redirect(url_for('index.homepage'))


@main.route('/register', methods=['POST'])
def register():
    u = User.validate_register(request.form)
    if u is None:
        message = '* 账号已存在或账号密码不规范,请重新注册'
        return render_template('index.html', message=message)
    message = '注册成功！'
    return render_template('index.html', message=message)


@main.route('/homepage')
def homepage():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    return render_template('home_page.html')

