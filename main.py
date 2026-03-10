import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder


API_TOKEN = "8702806640:AAHg8TOMEsOr0FsQzfLT2_VnVmM272DWz_s"


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Здравствуйте, {message.from_user.first_name}! Здесь вы можете ознакомиться с одним из моих '
                         f'проектов - ботом Алексис. В нем представлено несколько демонстративных функций, которые вы'
                         f'можете опробовать.')
    await message.answer('Ссылка на страничку на Kwork:')
    await message.answer('https://kwork.ru/user/_vladimir-')


# @dp.message(Command("show"))
# async def show(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(text="text", callback_data="1"))
#     await message.answer('', reply_markup=builder.as_markup())
#
#
# @dp.callback_query(F.data == "1")
# async def callback1(callback: types.CallbackQuery):
#     await callback.message.delete()
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(text="Назад", callback_data="2"))
#     await Bot(token=API_TOKEN).send_photo(chat_id=callback.message.chat.id,
#                                           photo=FSInputFile('1.png'),
#                                           reply_markup=builder.as_markup())
#     await callback.answer()
#
#
# @dp.callback_query(F.data == "2")
# async def callback2(callback: types.CallbackQuery):
#     await callback.message.delete()
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(text="text", callback_data="1"))
#     await Bot(token=API_TOKEN).send_message(chat_id=callback.message.chat.id,
#                                             text='',
#                                             reply_markup=builder.as_markup())


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())