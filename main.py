import asyncio
import aiosmtplib
import aiosqlite3
from email.message import EmailMessage
from datetime import datetime


async def sending(address, name):
    message = EmailMessage()
    message["From"] = "test@gmail.com"
    message["To"] = address
    message["Subject"] = "Рассылка"
    message.set_content(f"Уважаемый {name}!\nСпасибо, что пользуетесь нашим сервисом объявлений.")
    await aiosmtplib.send(message, hostname="127.0.0.1", port=2525)


async def main():
    async with aiosqlite3.connect('contacts.db') as con:
        select = await con.execute('SELECT * FROM contacts;')
        contacts = await select.fetchall()
        await asyncio.gather(*[sending(contact[3], contact[1]) for contact in contacts])


if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    now = datetime.now() - start
    print(now)
