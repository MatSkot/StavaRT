import datetime
import httpx
import logging
import traceback

from base64 import b64encode

from app.libs.models import RemoteRequest

logger = logging.getLogger()

async def get_remote(remote: RemoteRequest) -> RemoteRequest:

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                remote.method,
                remote.url,
                params=remote.params,
                headers=remote.headers,
                timeout=httpx.Timeout(remote.timeout))
            remote.response = response.content
        except httpx.ReadTimeout:
            logger.error(f"REQUEST TIMEOUT: {remote.url}")
        except Exception as e:
            logger.error(f"Request failed with: {e}\n{traceback.format_exc()}")

    return remote


def basic_auth(username, password):
    basic = b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    return f"Basic {basic}"


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)
