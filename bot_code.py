from aiogram import F, Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.requests import get_queue, create_chat, get_chat, delete_chat, delete_queue, add_queue

rt = Router()


@rt.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Подключиться", callback_data="connect")
    await message.answer("Нажми кнопку, чтобы подключиться к чату", reply_markup=kb.as_markup())


@rt.callback_query(F.data == "connect")
async def connect(call: types.CallbackQuery, bot: Bot):
    # user_id = call.from_user.id

    # if get_queue():
    #     await call.answer("Already connected")
    #     return

    # add_queue(user_id)
    # await call.answer("Connected")

    # chat = get_chat(user_id)

    partner = await get_queue()

    if await create_chat(call.from_user.id, partner) is False:
        await add_queue(call.from_user.id)

        markup = InlineKeyboardBuilder()
        markup.button(text="Отмена", callback_data="stop")

        await call.message.edit_text("Поиск...", reply_markup=markup.as_markup())

    else:
        await delete_queue(call.from_user.id)
        await delete_queue(partner)

    
        btn = [
            [types.KeyboardButton(text="Отключиться")]
        ]
        markup = types.ReplyKeyboardMarkup(
            keyboard=btn,
            resize_keyboard=True
        )
        await call.message.delete()
        await call.message.answer("Вы присоединились к чату!\nЧтобы отключиться, нажмите на кнопку ниже", reply_markup=markup)
        await bot.send_message(partner, "Вы присоединились к чату!\nЧтобы отключиться, нажмите на кнопку ниже", reply_markup=markup)
        


@rt.callback_query(F.data == "stop")
async def stop(call: types.CallbackQuery):
    await delete_queue(call.from_user.id)

    markup = InlineKeyboardBuilder()
    markup.button(text="Подключиться", callback_data="connect")

    await call.message.edit_text("Поиск остановлен!", reply_markup=markup.as_markup())


@rt.callback_query(F.data == "disconnect")
async def disconnect(call: types.CallbackQuery):
    await delete_chat(call.from_user.id)
    

    markup = InlineKeyboardBuilder()
    markup.button(text="Подключиться", callback_data="connect")

    await call.message.edit_text("Вы отключены!", reply_markup=markup.as_markup())




@rt.message(F.text == "Отключиться")
async def disconnect(message: types.Message, bot: Bot):
    await message.delete()
    await delete_chat(message.from_user.id)

    markup = InlineKeyboardBuilder()
    markup.button(text="Подключиться", callback_data="connect")
    kb = types.ReplyKeyboardRemove()

    await message.answer("Вы отключены!", reply_markup=kb)
    await message.answer("Нажми кнопку, чтобы подключиться к чату", reply_markup=markup.as_markup())


@rt.message(F.text)
async def anonim_send(message: types.Message, bot: Bot):
    
    chat = await get_chat(message.chat.id)
    await bot.send_message(chat[1], message.text)