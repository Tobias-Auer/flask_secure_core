# __init__.py
from .blueprints import bp


_connection_manager = None

def get_connection_manager():
    return _connection_manager

def _init_app(app):
    app.register_blueprint(bp,  template_folder="templates")

def init_fsl(app, db_type='postgres', db_name=None, db_user=None, db_password=None, db_host='localhost', db_port=5432, minconn=3, maxconn=10, recreate_db=False):
    global _connection_manager
    _init_app(app)

    if db_type == 'postgres':
        from .db.DBConnectionManagerPostgres import DBConnectionManager
        _connection_manager = DBConnectionManager(db_host=db_host, db_port=db_port, db_name=db_name, db_user=db_user, db_password=db_password, minconn=minconn, maxconn=maxconn, recreate_db=recreate_db)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
