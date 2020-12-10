from http import HTTPStatus

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from sanic.log import logger


BROKER_HOST_PREFIX = "Broker_"


class PinotClient(object):
    def __init__(self, loop):
        self.http = ClientSession(loop=loop, raise_for_status=True)

    async def _dispatch(self, method: str, url: str, headers: dict = None, json: dict = None):
        try:
            async with self.http.request(method, url, headers=headers, json=json) as rv:
                return await rv.json(), rv.status
        except ClientResponseError as exc:
            raise exc

    def _normalize_url(self, base, path):
        return "{0}/{1}".format(base.rstrip("/"), path.lstrip("/"))

    async def get_tenant_list(self, controller_url: str):
        url = self._normalize_url(controller_url, "/v2/brokers/tenants")
        tenants = {}
        data, status = await self._dispatch("GET", url)
        if status != HTTPStatus.OK:
            logger.warning(
                "Failed to fetch tenant addresses",
                extra={
                    "status_code": status,
                    "response": data,
                },
            )

        for name, brokers in data.items():
            tenants[name] = [
                "http://{0}:{1}".format(
                    broker["host"].replace(BROKER_HOST_PREFIX, ""), broker["port"]
                )
                for broker in brokers
            ]
        return tenants

    async def execute_pql_query(self, broker_url, data):
        url = self._normalize_url(broker_url, "/query")
        return await self._dispatch("POST", url, json=data)

    async def execute_sql_query(self, broker_url, data):
        url = self._normalize_url(broker_url, "/query/sql")
        return await self._dispatch("POST", url, json=data)

    async def close(self):
        await self.http.close()


async def close_pinot_session(app, loop):
    loop.run_until_complete(app.pinot_client.close())
    loop.close()


async def open_pinot_session(app, loop):
    app.pinot_client = PinotClient(loop)
