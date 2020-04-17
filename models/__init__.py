from pymongo import MongoClient
import time
from utils import log

mongua = MongoClient()


def now_time():
    dt = time.localtime(int(time.time()))
    dt_format = "%Y-%m-%d %H:%M:%S"
    return time.strftime(dt_format, dt)


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = mongua.db['User_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongua(object):
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('id', int, -1),
        ('type', str, ''),
        ('created_time', str, 0),
        ('updated_time', str, 0),
    ]

    @classmethod
    def new(cls, form=None):
        name = cls.__name__
        if form is None:
            form = {}
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)
        m.id = next_id(name)
        m.type = name.lower()
        ts = now_time()
        m.created_time = ts
        m.updated_time = ts
        m.save()
        return m

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def _find_raw(cls, **kwargs):         # 根据传进的kwargs返回相应的字典列表
        name = cls.__name__
        return list(mongua.db[name].find(kwargs))

    @classmethod
    def _find(cls, **kwargs):             # 根据传进的kwargs返回相应的实例组
        name = cls.__name__
        ds = mongua.db[name].find(kwargs)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def _new_with_bson(cls, bson):              # 相当于以前的传入一个数据库的form生成一个object
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        # 这一句必不可少，否则 bson 生成一个新的_id
        # FIXME, 因为现在的数据库里面未必有 type
        # 所以在这里强行加上
        # 以后洗掉db的数据后应该删掉这一句
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def find_by(cls, **kwargs):     # 根据kwargs 返回一个实例
        name = cls.__name__
        dict = mongua.db[name].find_one(kwargs)
        if dict is None:
            return None
        return cls._new_with_bson(dict)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def update(cls, form, **kwargs):
        name = cls.__name__
        dict = {
            '$set': form,
        }
        mongua.db[name].update_one(kwargs, dict)
        return cls.find_by(**kwargs)

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        condition = {
            'id': id,
        }
        m = cls.find_by(id=id)
        if m is None:
            return None
        mongua.db[name].delete_one(condition)
        return m

    def save(self):
        name = self.__class__.__name__
        mongua.db[name].insert_one(self.__dict__)   # 在这里用了insert之后self自动加了_id的属性.

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))