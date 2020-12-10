from http import HTTPStatus

from aiohttp.client_exceptions import ClientResponseError
from sanic import Blueprint
from sanic.response import json

from pinot_rest_proxy import get_revision, get_version, settings


INVALID_PQL_QUERY_BODY_ERR_MSG = "Invalid request body, tenant and pql are required."
INVALID_SQL_QUERY_BODY_ERR_MSG = "Invalid request body, tenant and sql are required."
TENANT_NOT_FOUND_ERR_MSG = "Tenant not found"

blueprint = Blueprint("views")


@blueprint.get("/")
async def index(request):
    return json({"revision": get_revision(), "version": get_version()})


@blueprint.get("/tenants")
async def list_tenants(request):
    try:
        return json(await request.app.pinot_client.get_tenant_list(settings.PINOT_CONTROLLER_URL))
    except ClientResponseError as exc:
        return json({"msg": exc.message}, status=exc.status)


@blueprint.post("/query")
async def execute_pql(request):
    tenant = request.json.get("tenant")
    pql = request.json.get("pql")

    if not tenant or not pql:
        return json({"msg": INVALID_PQL_QUERY_BODY_ERR_MSG}, status=HTTPStatus.BAD_REQUEST)
    elif tenant not in request.app.tenants:
        return json({"msg": TENANT_NOT_FOUND_ERR_MSG}, status=HTTPStatus.BAD_REQUEST)

    brokers = request.app.tenants.get(tenant)
    try:
        data, status = await request.app.pinot_client.execute_pql_query(next(brokers), {"pql": pql})
        return json(data, status=status)
    except ClientResponseError as exc:
        return json({"msg": exc.message}, status=exc.status)


@blueprint.post("/query/sql")
async def execute_sql(request):
    tenant = request.json.get("tenant")
    sql = request.json.get("sql")

    if not tenant or not sql:
        return json({"msg": INVALID_SQL_QUERY_BODY_ERR_MSG}, status=HTTPStatus.BAD_REQUEST)
    elif tenant not in request.app.tenants:
        return json({"msg": TENANT_NOT_FOUND_ERR_MSG}, status=HTTPStatus.BAD_REQUEST)

    brokers = request.app.tenants.get(tenant)
    try:
        data, status = await request.app.pinot_client.execute_sql_query(next(brokers), {"sql": sql})
        return json(data, status=status)
    except ClientResponseError as exc:
        return json({"msg": exc.message}, status=exc.status)
