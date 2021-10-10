from .. import loader, utils
from telethon import functions

@loader.tds
class RenameMod(loader.Module):
    """Переиминовать или добавить чела в контакт."""
    strings={"name": "Rename"}

    async def renamecmd(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Где аргументы дыбил.</b>")
        if not reply:
            return await message.edit("<b>Реплай сделай дыбил.</b>")
        else:
            user = await message.client.get_entity(reply.sender_id)
        try:
            await message.client(functions.contacts.AddContactRequest(id=user.id, 
                                                                      first_name=args,
                                                                      last_name=' ',
                                                                      phone='мобила',
                                                                      add_phone_privacy_exception=False))
            await message.edit(f"<code>{user.id}</code> переименован(-а) на <code>{args}</code>")
        except: return await message.edit("<b>Что то пошло по пизде.</b>")