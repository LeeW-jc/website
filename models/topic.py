from . import Mongua
from .reply import Reply
from utils import log
import redis
import logging
import json
from .user import User
ogger = logging.getLogger("website")


class RedisCache(object):
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Topic(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('user_id', int, -1),
        ('title', str, ''),
        ('content', str, ''),
        ('views', int, 0),
    ]
    should_update_all = True
    redis_cache = RedisCache()

    def save(self):              # Mongo的save方法为mongo的insert_one方法,new()方法会用到save这样就自动True了
        super().save()
        Topic.should_update_all = True

    @classmethod
    def delete(cls, id):
        t = super().delete(id)
        Topic.should_update_all = True
        return t

    @classmethod
    def get(cls, id):
        t = Topic.find_by(id=id)
        if t is None:
            return None
        form = {
            'views': t.views + 1
        }
        tt = Topic.new_update(form, id=id)
        return tt

    @classmethod
    def replies(cls, tid):
        return Reply.find_all(topic_id=tid)

    def user(self):
        return User.find_by(id=self.user_id)

    @classmethod
    def new_update(cls, form, **kwargs):
        t = super().update(form, **kwargs)
        Topic.should_update_all = True
        return t

    @classmethod
    def new_all(cls):
        if Topic.should_update_all:
            ts = Topic.all()
            if not ts:
                return ts
            t_list = []
            for t in ts:
                d = t.__dict__
                d.pop('_id')
                t_list.append(d)
            Topic.redis_cache.set('all_topic', json.dumps(t_list))
            Topic.should_update_all = False
            return ts
        d_list = json.loads(Topic.redis_cache.get('all_topic').decode('utf-8'))
        t_list = []
        for d in d_list:
            t_list.append(Topic.change(d))
        return t_list

    @classmethod
    def change(cls, d):
        topic = Topic()
        fields = Topic.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in d:
                setattr(topic, k, t(d[k]))
            else:
                setattr(topic, k, v)
        return topic

