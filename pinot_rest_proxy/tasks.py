import asyncio

from pinot_rest_proxy import settings
from pinot_rest_proxy.exceptions import SettingsError


MISSING_PINOT_CONTROLLER_URL_ERR_MSG = "PINOT_CONTROLLER_URL is a required property."


async def fetch_tenants_task(app):
    while True:
        if not settings.PINOT_CONTROLLER_URL:
            raise SettingsError(MISSING_PINOT_CONTROLLER_URL_ERR_MSG)

        app.tenants = await app.pinot_client.get_tenant_list(settings.PINOT_CONTROLLER_URL)
        await asyncio.sleep(app.config["ROUTING_REFRESH_INTERVAL"])
