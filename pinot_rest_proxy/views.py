from aiohttp.client_exceptions import ClientResponseError
from sanic import Blueprint
from sanic.response import json

from pinot_rest_proxy import get_revision, get_version


INVALID_PQL_QUERY_BODY_ERR_MSG = ""
INVALID_SQL_QUERY_BODY_ERR_MSG = ""
TENANT_NOT_FOUND_ERR_MSG = "Tenant not found"

blueprint = Blueprint("views")


@blueprint.get("/")
async def index(request):
    return json({"revision": get_revision(), "version": get_version()})


@blueprint.get("/tenants")
async def list_tenants(request):
    return json(request.app.tenants)


@blueprint.post("/query")
async def execute_pql(request):
    tenant = request.json.get("tenant")
    pql = request.json.get("pql")

    if not tenant or not pql:
        return json({"msg": INVALID_PQL_QUERY_BODY_ERR_MSG})
    elif tenant not in request.app.tenants:
        return json({"msg": TENANT_NOT_FOUND_ERR_MSG})

    brokers = request.app.tenants.get(tenant)

    # TODO:
    # Load balance between brokers
    return await request.app.pinot_client.execute_pql_query(brokers[0], {"pql": pql})


@blueprint.post("/query/sql")
async def execute_sql(request):
    tenant = request.json.get("tenant")
    sql = request.json.get("sql")

    if not tenant or not sql:
        return json({"msg": INVALID_SQL_QUERY_BODY_ERR_MSG})
    elif tenant not in request.app.tenants:
        return json({"msg": TENANT_NOT_FOUND_ERR_MSG})

    brokers = request.app.tenants.get(tenant)

    # TODO:
    # Load balance between brokers
    return await request.app.pinot_client.execute_sql_query(brokers[0], {"sql": sql})
