from .. import loader, utils
from telethon import functions, types


def register(cb):
    cb(WhoMod())


class WhoMod(loader.Module):
    """Получает информацию о пользователе. by seen"""
    strings = {"name": "Who",
               "text_who": "<b>Name:</b> <code>{}</code>.\n<b>ID:</b> <code>{}</code>.\n<b>User:</b> @{}.",
               "none": "<b>Пользователь не найден.</b>"}

    async def whocmd(self, message):
        """Используй .who <@,id или реплай>"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        try:
            if message.is_private:
                user = await message.client.get_entity(message.chat_id) 
            else:
                if reply:
                    user = await message.client.get_entity(reply.sender_id)
                else:
                    user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            await utils.answer(message, self.strings["text_who"].format(user.first_name, user.id, user.username))
        except: return await utils.answer(message, self.strings["none"])