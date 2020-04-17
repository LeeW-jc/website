from . import Mongua
import logging
import json
import redis
from .user import User
ogger = logging.getLogger("website")


class RedisCache(object):
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Reply(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('user_id', int, -1),
        ('content', str, ''),
        ('topic_id', int, -1)
    ]
    redis_reply = RedisCache()
    should_update_all = True

    def save(self):              # Mongo的save方法为mongo的insert_one方法,new()方法会用到save这样就自动True了
        super().save()
        Reply.should_update_all = True

    @classmethod
    def delete(cls, id):
        t = super().delete(id)
        Reply.should_update_all = True
        return t

    @classmethod
    def new_update(cls, form, **kwargs):
        r = super().update(form, **kwargs)
        Reply.should_update_all = True
        return r

    @classmethod
    def new_all(cls):
        if Reply.should_update_all:
            rs = Reply.all()
            if not rs:
                return rs
            r_list = []
            for t in rs:
                d = t.__dict__
                d.pop('_id')
                r_list.append(d)
            Reply.redis_reply.set('all_reply', json.dumps(r_list))
            Reply.should_update_all = False
            return rs
        d_list = json.loads(Reply.redis_reply.get('all_reply').decode('utf-8'))
        r_list = []
        for d in d_list:
            r_list.append(Reply.change(d))
        return r_list

    @classmethod
    def change(cls, d):
        reply = Reply()
        fields = Reply.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in d:
                setattr(reply, k, t(d[k]))
            else:
                setattr(reply, k, v)
        return reply
