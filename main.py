import asyncio
import logging
import sys
import datetime as dt

from data import ADMIN, API_TOKEN

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Подключаем все необходимые библиотеки


dp = Dispatcher()


@dp.message(CommandStart()) # функция, обрабатывающая start - приветствие, краткое описание, список команд
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Здравствуйте, {message.from_user.first_name}! Здесь вы можете ознакомиться с одним из моих '
                         f'проектов - ботом Алексис. В нем представлено несколько демонстративных функций, которые вы'
                         f'можете опробовать.')
    await Bot(token=API_TOKEN).send_message(text=f'{message.from_user.first_name} started bot. '
                                                 f'{dt.datetime.now().strftime("%H:%M")}', chat_id=ADMIN)
    await message.answer('Ссылка на страничку на Kwork:')
    await message.answer('https://kwork.ru/user/_vladimir-')
    await message.answer('Список актуальных команд для бота:'
                         '\n/parse - парсинг курса валют в данный момент')


@dp.message(Command('parse')) # парсинг сайта ЦБ РФ с курсом валют
async def value_parsing(message: Message) -> None:

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options) # обращаемся к сайту, берем код html
    driver.get("https://cbr.ru/curreNcy_base/daily/")

    text = 'Цифр. код - Букв. код - Единиц - Валюта - Курс'
    for i in driver.page_source.split('<tbody>')[2].split('</tbody>')[0].split('<tr>'):
        if 'td' in i:
            element = []
            for j in i.split('</tr>')[0].split('</td>'):
                if 'td' in j:
                    element.append(j.split()[0][4:])
            text += f'\n\n{' - '.join(element)}'
    driver.quit()
    await message.answer(text=text)
    await message.answer('Если хотите проверить достоверность информации, можете зайти в источник по ссылке ниже.')
    await message.answer('https://cbr.ru/curreNcy_base/daily/')


@dp.message(Command('kwork_link')) # при желании еще раз даем ссылку на профиль на Kwork
async def kwork_link(message: Message) -> None:
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