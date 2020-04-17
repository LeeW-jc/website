from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
)
from utils import format_content
import json
from models.topic import Topic
from models.reply import Reply

from . import current_user

main = Blueprint('reply', __name__)


@main.route('/api/all', methods=['GET'])
def all_reply():
    tid = int(request.args['topic_id'])
    rs = Topic.replies(tid)
    # replies = [r.__dict__ for r in rs]
    replies = []
    for r in rs:
        d = r.__dict__
        d.pop('_id')
        replies.append(d)
    return json.dumps(replies)            # 不能有_id.


@main.route('/api/add', methods=['POST'])
def add():
    form = json.loads(request.data.decode('utf-8'))
    form['content'] = format_content(form['content'])
    api_form = Reply.new(form).__dict__
    api_form.pop('_id')
    return json.dumps(api_form)

