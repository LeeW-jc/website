from . import Mongua
import hashlib
from utils import log


class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, 'default.png'),
        ('dpcq', int, -1),
        ('dldl', int, -1),
    ]

    @classmethod
    def validate_register(cls, form):
        username = form.get('username')
        password = form.get('password')
        user = User.find_by(username=username)
        if user is None and 3 < len(username) < 18 and 3 < len(password) < 18:
            new_form = {
                'username': username,
                'password': User.salted_password(password),
            }
            u = User.new(new_form)
            return u
        return None

    @classmethod
    def validate_login(cls, form):
        username = form.get('username')
        password = form.get('password')
        user = User.find_by(username=username)
        if user is not None and User.salted_password(password) == user.password:
            return user
        return None

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        pwd = sha256(password)
        secret_pwd = sha256(pwd + salt)
        return secret_pwd

