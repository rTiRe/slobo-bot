import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI
from starlette_context import middleware, plugins

from config.settings import settings
from src import api, background_tasks, bot, handlers

import logging

logging.basicConfig(level=logging.INFO)


async def setup_app() -> tuple[Dispatcher, Bot]:
    dp = Dispatcher()
    bot.setup_dp(dp)
    dp.include_router(handlers.router)
    default = DefaultBotProperties(parse_mode=enums.ParseMode.HTML)
    tg_bot = Bot(token=settings.BOT_TOKEN, default=default)
    bot.setup_bot(tg_bot)
    return dp, tg_bot


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _dp, tg_bot = await setup_app()
    await tg_bot.set_webhook(settings.bot_webhook_url)
    yield
    while background_tasks:
        await asyncio.sleep(0)
    await tg_bot.delete_webhook()


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(api.router)
    app.add_middleware(
        middleware.RawContextMiddleware,
        plugins=[plugins.CorrelationIdPlugin()],
    )
    return app


async def start_polling() -> None:
    dp, tg_bot = await setup_app()
    await tg_bot.delete_webhook()
    await dp.start_polling(tg_bot)


if __name__ == '__main__':
    if settings.FASTAPI_HOST:
        uvicorn.run(
            'src.app:create_app',
            factory=True,
            host='0.0.0.0',
            port=settings.FASTAPI_PORT,
            workers=1,
        )
    else:
        asyncio.run(start_polling())
