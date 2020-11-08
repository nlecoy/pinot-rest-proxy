from pinot_rest_proxy import settings
from pinot_rest_proxy.app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
