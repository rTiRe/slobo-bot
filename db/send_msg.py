from aio_pika import connect, Message
from dotenv import load_dotenv
from os import getenv
import asyncio

load_dotenv()

async def main():
    connection = await connect(host='127.0.0.1', login = getenv('RABBIT_DEFAULT_USER'), password=getenv('RABBIT_DEFAULT_PASS'), port=int(getenv('RABBIT_PORT')) )
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("send_")
        await channel.default_exchange.publish(
            Message(b"Hello World!"),
            routing_key=queue.name,
        )
        print(" [x] Sent 'Hello World!'")




if __name__ == "__main__":
    asyncio.run(main())