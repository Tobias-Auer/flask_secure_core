from .blueprints import bp
from .get_conn import get_connection_manager, set_connection_manager
from .decorators import AuthDecorators

def _init_app(app):
    app.register_blueprint(bp, template_folder="templates")
    authDecorators = AuthDecorators()
    app.require_login = authDecorators.require_login
    app.require_permission = authDecorators.require_permission



def init_fsl(app, db_type='postgres', db_name=None, db_user=None, db_password=None,
             db_host='localhost', db_port=5432, minconn=3, maxconn=10, recreate_db=False):
    global _connection_manager

    if db_type == 'postgres':
        from .db.DBConnectionManagerPostgres import DBConnectionManager
        manager = DBConnectionManager(
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
            minconn=minconn,
            maxconn=maxconn,
            recreate_db=recreate_db
        )
        set_connection_manager(manager)
        _init_app(app)

    else:
        raise ValueError(f"Unsupported database type: {db_type}")
