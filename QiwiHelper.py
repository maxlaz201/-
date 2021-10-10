from .. import loader, utils
from SimpleQIWI import QApi

data = {
        "643": "RUB",
        "840": "USD",
        "978": "EUR",
        "398": "KZT"
        }

@loader.tds
class QiwiMod(loader.Module):
    """получаем инфу о киви"""
    strings = {'name': 'QiwiHelper'}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def setqncmd(self, message):
        """Используй: .setqn «номер» чтобы установить номер киви кошелька."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("<b>Где аргументы?</b>")
        self.db.set("qiwi", "number", args)
        await message.edit("<b>Номер киви успешно установлен.</b>")

    async def setqtcmd(self, message):
        """Используй: .setqt «токен» чтобы установить токен от киви."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("<b>Где аргументы?</b>")
        self.db.set("qiwi", "token", args)
        await message.edit("<b>Токен от киви успешно установлен.</b>")

    async def qiwicmd(self, message):
        """Используй: .qiwi чтобы посмотреть информацию кошелька."""
        await message.edit("<b>Загрузка...</b>")
        number = self.db.get("qiwi", "number")
        token = self.db.get("qiwi", "token")
        if not number or not token:
            return await message.edit("<b>Ты не заполнил токен или номер.</b>")
        try:
            api = QApi(token=token, phone=number)
            p = api.payments['data'][0]
            last = f"{str(p['sum']['amount'])} {data[str(p['sum']['currency'])]}"
            for f in api.full_balance:
                b = f['balance']
                balance = f"{str(b['amount'])} {data[str(b['currency'])]}"
            await message.edit(f"💰 <b>Мой баланс QIWI:</b>\n<code>{balance}</code>\n\n"
                               f"💸 <b>Последнee получение денег:</b>\n<code>{last}</code>")
        except: return await message.edit("<b>Произошла ошибка, проверь все ли данные ты ввёл верно.</b>")

    async def sendqiwicmd(self, message):
        """Используй: .sendqiwi «номер» «сумма» чтобы перевести денег."""
        number = self.db.get("qiwi", "number")
        token = self.db.get("qiwi", "token")
        api = QApi(token=token, phone=number)
        args = utils.get_args_raw(message)
        if not number or not token:
            return await message.edit("<b>Ты не заполнил токен или номер.</b>")
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        sendto = utils.get_args(message)[0]
        sendamount = utils.get_args(message)[1]
        comment = args.split(sendamount)[1] or "Pay!"
        if not sendto or not sendamount or not sendamount.isdigit():
            return await message.edit("<b>Аргументы введены не верно.</b>")
        try:
            api.pay(account=sendto, amount=int(sendamount), comment=comment)
            await message.edit("💸 <b>Перевёл успешно!</b>")
        except:
            return await message.edit("❌ <b>Не удалось перевести деньги!</b>")