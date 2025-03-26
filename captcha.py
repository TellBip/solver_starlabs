import asyncio
from loguru import logger
from primp import AsyncClient
import requests
from typing import Optional, Dict
from enum import Enum
import time
import re


class CaptchaError(Exception):
    """Base exception for captcha errors"""

    pass


class ErrorCodes(Enum):
    ERROR_WRONG_USER_KEY = "ERROR_WRONG_USER_KEY"
    ERROR_KEY_DOES_NOT_EXIST = "ERROR_KEY_DOES_NOT_EXIST"
    ERROR_ZERO_BALANCE = "ERROR_ZERO_BALANCE"
    ERROR_PAGEURL = "ERROR_PAGEURL"
    IP_BANNED = "IP_BANNED"
    ERROR_PROXY_FORMAT = "ERROR_PROXY_FORMAT"
    ERROR_BAD_PARAMETERS = "ERROR_BAD_PARAMETERS"
    ERROR_BAD_PROXY = "ERROR_BAD_PROXY"
    ERROR_SITEKEY = "ERROR_SITEKEY"
    CAPCHA_NOT_READY = "CAPCHA_NOT_READY"
    ERROR_CAPTCHA_UNSOLVABLE = "ERROR_CAPTCHA_UNSOLVABLE"
    ERROR_WRONG_CAPTCHA_ID = "ERROR_WRONG_CAPTCHA_ID"
    ERROR_EMPTY_ACTION = "ERROR_EMPTY_ACTION"


class Solvium:
    def __init__(
            self,
            api_key: str,
            session: AsyncClient,
            proxy: Optional[str] = None,
    ):
        self.api_key = api_key
        self.proxy = proxy
        self.base_url = "http://localhost:5000"
        self.session = session

    def _format_proxy(self, proxy: str) -> str:
        if not proxy:
            return None
        if "@" in proxy:
            return proxy
        return f"http://{proxy}"

    async def create_turnstile_task(self, sitekey: str, pageurl: str) -> Optional[str]:
        """Creates a Turnstile captcha solving task using local API server"""
        url = f"{self.base_url}/turnstile?url={pageurl}&sitekey={sitekey}"


        try:
            response = await self.session.get(url, timeout=30)
            #logger.debug(f"Response status: {response.status_code}")
            #logger.debug(f"Raw response: {response.text}")

            try:
                result = response.json()
            except ValueError as e:
                logger.error(f"Failed to parse response as JSON: {response.text}")
                raise e

            if "task_id" in result:
                return result["task_id"]

            logger.error(f"Error creating Turnstile task with local API: {result}")
            return None

        except Exception as e:
            logger.error(f"Error creating Turnstile task with local API: {e}")
            return None

    async def get_task_result(self, task_id: str) -> Optional[str]:
        """Gets the result of the captcha solution from local API server"""
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = await self.session.get(
                    f"{self.base_url}/result?id={task_id}",
                    timeout=30,
                )

                # Логируем статус и сырой ответ
                #logger.debug(f"Response status: {response.status_code}")
                #logger.debug(f"Raw response: {response.text}")

                # Проверяем статус ответа
                if response.status_code not in (200, 202):
                    logger.error(f"Unexpected status code: {response.status_code}, response: {response.text}")
                    return None

                # Проверяем содержимое ответа
                raw_response = response.text.strip()

                # Если ответ — это строка "CAPTCHA_NOT_READY", продолжаем ждать
                if raw_response == "CAPTCHA_NOT_READY":
                    #logger.debug(f"Task {task_id} is still processing, attempt {attempt + 1}/{max_attempts}")
                    await asyncio.sleep(10)
                    continue

                # Пробуем разобрать ответ как JSON
                try:
                    result = response.json()
                except ValueError as e:
                    logger.error(f"Failed to parse response as JSON: {raw_response}")
                    return None

                # Проверяем, есть ли решение
                if result.get("value"):
                    solution = result["value"]

                    # Проверяем, что решение содержит только допустимые символы
                    if re.match(r'^[a-zA-Z0-9\.\-_]+$', solution):
                        return solution
                    else:
                        logger.error(f"Invalid solution format from local API: {solution}")
                        return None

                # Если в ответе ошибка
                if result.get("status") == "error":
                    logger.error(f"Error from API: {result.get('error', 'Unknown error')}")
                    return None

                # Если статус не "pending", но нет решения, логируем и продолжаем
                #logger.debug(f"Task {task_id} is still processing, waiting... Response: {result}")
                await asyncio.sleep(10)
                continue

            except Exception as e:
                logger.error(f"Error getting result with local API: {e}")
                return None

        logger.error("Max polling attempts reached without getting a result with local API")
        return None

    async def solve_captcha(self, sitekey: str, pageurl: str) -> Optional[str]:
        """Solves Cloudflare Turnstile captcha and returns token using local API server"""
        task_id = await self.create_turnstile_task(sitekey, pageurl)
        if not task_id:
            return None

        return await self.get_task_result(task_id)
