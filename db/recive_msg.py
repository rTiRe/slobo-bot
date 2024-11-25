import asyncio
from aio_pika import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()

async def on_message(message):
    async with message.process():
        print(f" [x] Received message: {message.body.decode()}")

async def main():
    connection = await connect(host='127.0.0.1', login = getenv('RABBIT_DEFAULT_USER'), password=getenv('RABBIT_DEFAULT_PASS'), port=int(getenv('RABBIT_PORT')))
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("send_")
        await queue.consume(on_message)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()



if __name__ == "__main__":
    asyncio.run(main())
