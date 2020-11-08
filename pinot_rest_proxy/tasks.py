import asyncio
import itertools

from pinot_rest_proxy import settings
from pinot_rest_proxy.exceptions import SettingsError


MISSING_PINOT_CONTROLLER_URL_ERR_MSG = "PINOT_CONTROLLER_URL is a required property."


async def fetch_tenants_task(app):
    prev_tenant_state = {}
    while True:
        if not settings.PINOT_CONTROLLER_URL:
            raise SettingsError(MISSING_PINOT_CONTROLLER_URL_ERR_MSG)

        tenants = await app.pinot_client.get_tenant_list(settings.PINOT_CONTROLLER_URL)
        if not tenants == prev_tenant_state:
            iter_tenants = {}
            prev_tenant_state = tenants
            for tenant, brokers in tenants.items():
                iter_tenants[tenant] = itertools.cycle(brokers)
            app.tenants = iter_tenants
        await asyncio.sleep(app.config["ROUTING_REFRESH_INTERVAL"])
