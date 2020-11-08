from sanic import Sanic

from pinot_rest_proxy import settings, views
from pinot_rest_proxy.client import close_pinot_session, open_pinot_session
from pinot_rest_proxy.tasks import fetch_tenants_task


def create_app():
    app = Sanic("pinot_rest_proxy")

    app.config.from_object(settings)

    register_listeners(app)
    register_background_tasks(app)
    register_blueprints(app)

    return app


def register_background_tasks(app):
    app.add_task(fetch_tenants_task)


def register_blueprints(app):
    app.blueprint(views.blueprint)


def register_listeners(app):
    app.register_listener(open_pinot_session, "before_server_start")
    app.register_listener(close_pinot_session, "after_server_stop")
