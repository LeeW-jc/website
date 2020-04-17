from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from models.story import Story
from models.user import User
from . import current_user
from utils import (
    style,
    format_content,
)
import json

main = Blueprint('story', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    story_name = 'dpcq'
    if u.dpcq == -1:
        s = Story.find_by(story_name=story_name, page=1)
    else:
        s = Story.find_by(story_name=story_name, page=u.dpcq)
    tag_story = 'dpcq'
    return render_template('story/story_index.html', title=s.title,
                           content=s.content, style_dldl='', style_dpcq=style[1], tag_story=tag_story)


@main.route('/new')
def new():
    u = current_user()
    if u.id != 1:
        return redirect(url_for('index.homepage'))
    return render_template('story/story_add.html')


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u.id != 1:
        return redirect(url_for('index.homepage'))
    form = dict(request.form)
    form['content'] = format_content(form['content'])
    Story.new(form)
    return redirect(url_for('story.index'))


@main.route('/api/dpcq/next')
def dpcq_next():
    u = current_user()
    if u.dpcq == 1912:
        page = 1912
        s = Story.find_by(story_name='dpcq', page=page)
    elif u.dpcq == -1:
        page = 2
        s = Story.find_by(story_name='dpcq', page=page)
    else:
        page = u.dpcq + 1
        s = Story.find_by(story_name='dpcq', page=page)
    user_update = {
        'dpcq': page,
    }
    User.update(user_update, id=u.id)
    form = {
        'title': s.title,
        'content': s.content,
    }
    return json.dumps(form)


@main.route('/api/dpcq/last')
def dpcq_last():
    u = current_user()
    if u.dpcq == -1 or u.dpcq == 1:
        page = 1
        s = Story.find_by(story_name='dpcq', page=page)
    else:
        page = u.dpcq - 1
        s = Story.find_by(story_name='dpcq', page=page)
    user_update = {
        'dpcq': page,
    }
    User.update(user_update, id=u.id)
    form = {
        'title': s.title,
        'content': s.content,
    }
    return json.dumps(form)


@main.route('/api/dldl/next')
def dldl_next():
    u = current_user()
    if u.dldl == 738:
        page = 738
        s = Story.find_by(story_name='dldl', page=page)
    elif u.dldl == -1:
        page = 2
        s = Story.find_by(story_name='dldl', page=page)
    else:
        page = u.dldl + 1
        s = Story.find_by(story_name='dldl', page=page)
    user_update = {
        'dldl': page,
    }
    User.update(user_update, id=u.id)
    form = {
        'title': s.title,
        'content': s.content,
    }
    return json.dumps(form)


@main.route('/api/dldl/last')
def dldl_last():
    u = current_user()
    if u.dldl == -1 or u.dldl == 1:
        page = 1
        s = Story.find_by(story_name='dldl', page=page)
    else:
        page = u.dldl - 1
        s = Story.find_by(story_name='dldl', page=page)
    user_update = {
        'dldl': page,
    }
    User.update(user_update, id=u.id)
    form = {
        'title': s.title,
        'content': s.content,
    }
    return json.dumps(form)


@main.route('/dldl')
def dldl_index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    story_name = 'dldl'
    if u.dldl == -1:
        s = Story.find_by(story_name=story_name, page=1)
    else:
        s = Story.find_by(story_name=story_name, page=u.dldl)
    tag_story = 'dldl'
    return render_template('story/story_index.html', title=s.title,
                           content=s.content, style_dldl=style[0], style_dpcq='', tag_story=tag_story)
