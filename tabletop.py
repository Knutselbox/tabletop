import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Post
from app import socketio

#if __name__ == '__main__':
app = create_app()
socketio.run(app, debug=False, host='0.0.0.0', port=5000)



@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
