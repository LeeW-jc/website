from flask import Flask
import config
from routes.index import main as index_route
from routes.topic import main as topic_route
from routes.story import main as story_route
from routes.reply import main as reply_route


app = Flask(__name__)
app.secret_key = config.secret_key


app.register_blueprint(index_route)
app.register_blueprint(topic_route, url_prefix='/topic')
app.register_blueprint(story_route, url_prefix='/story')
app.register_blueprint(reply_route, url_prefix='/reply')


if __name__ == '__main__':
    connection_config = dict(
        host='0.0.0.0',
        port=3000,
        debug=True,
    )
    app.run(**connection_config)





