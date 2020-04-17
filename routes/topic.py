# coding=utf8
from flask import (
    Blueprint,
    redirect,
    abort,
    render_template,
    request,
    url_for,
)
from utils import (
    format_content,
    random_background,
)
import redis
from models.topic import (
    Topic,
)
from . import current_user
import uuid

main = Blueprint('topic', __name__)
token = dict()
redis_video_db = redis.StrictRedis(host='localhost', port=6379, db=0)
jump_video = True
jump_img = True


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    ts = Topic.new_all()
    ts.reverse()
    topic_background = random_background()
    return render_template('topic/topic_index.html', topics=ts, topic_background=topic_background)


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    t = Topic.get(id)
    tid = id
    if u.id == t.user_id:
        display = "inline"
        key = "{}".format(uuid.uuid4())
        token[key] = u.username
        delete_background = random_background()
        return render_template('topic/detail.html', t=t, delete_background=delete_background,
                               display=display, token=key, id_user=u.id, tid=tid)
    else:
        display = "none"
        return render_template('topic/detail.html', t=t, display=display,
                               token='', id_user=u.id, tid=tid)


@main.route('/new')
def new():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    user_id = u.id
    return render_template('topic/new.html', uid=user_id)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    if request.form['title'] == '':
        return redirect(url_for('topic.new'))
    form = dict(request.form)
    form['content'] = format_content(form['content'])
    Topic.new(form)
    return redirect(url_for('topic.index'))


@main.route('/delete')
def delete():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    tid = int(request.args['id'])
    validate_token = request.args['token']
    if token[validate_token] != u.username:
        return redirect(url_for('topic.index'))
    Topic.delete(tid)
    token.pop(validate_token)
    return redirect(url_for('topic.index'))


# 静态且不变的文件可以直接在程序启动时发给redis，在load路由只用get redis的数据就行.
@main.route('/static')
def load_video():
    if request.args['file'] == 'bili2.mp4':
        global jump_video
        if jump_video:
            with open('static/IMG/bili2.mp4', 'rb') as f:
                ff = f.read()
                redis_video_db.set('video', ff)
            jump_video = False
            return ff
        return redis_video_db.get('video')
    elif request.args['file'] == 'heart':
        global jump_img
        if jump_img:
            with open('static/IMG/heart.png', 'rb') as f:
                ff = f.read()
                redis_video_db.set('img', ff)
            jump_img = False
            return ff
        return redis_video_db.get('img')
    else:
        abort(404)
