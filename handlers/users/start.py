from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import aiohttp
from keyboards.inline.authBtn import authBtn

from loader import dp
from states.states import AuthState

async def get_code(phone):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/resend_code/', json={"phone": f"+{phone}"}) as response:
            response_data = await response.json()
            print(response_data)
            if response.status == 200:
                if response_data.get('code'):
                    message = f"Tasdiqlash kodi: <b>{response_data.get('code')}</b>"
            elif response.status >= 500:
                message = f"Xatolik yuz berdi"
            else:
                message = "Siz kiritgan raqam ro'yhatdan o'tmagan"
            return message, response_data.get('guid')
        

async def verify(code, guid):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/verify/', json={"code": f"{code}", "guid": f"{guid}",}) as response:
            response_data = await response.json()
            print(response_data)
            if response.status == 200:
                if response_data.get('access') and response_data.get('refresh'):
                    message = f"""Login qilgandan kerakli malumotlar:\n\n<b>id:</b> {response_data.get('id')}\n<b>guid:</b> {response_data.get('guid')}\n<b>phone:</b> {response_data.get('phone')}\n<b>name:</b> {response_data.get('name')}\n<b>access:</b> {response_data.get('access')}\n<b>refresh:</b> {response_data.get('refresh')}"""
            elif response.status >= 500:
                message = f"Xatolik yuz berdi"
            else:
                message = "Siz kiritgan kod mos kelmadi, qayta urinib ko'ring."
            return message
            
                    

@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    phone = message.get_args()
    if phone:
        msg = await get_code(phone)
        await message.answer(msg[0])
        return
    await message.answer("Telefon raqamingizni yuboring. Masalan: 998901321921")
    await AuthState.phone.set()
            
                    

@dp.message_handler(commands=['login'], state="*")
async def login(message: types.Message, state=FSMContext):
    await message.answer("Telefon raqamingizni yuboring. Masalan: 998901321921")
    await AuthState.phone.set()
    

@dp.message_handler(state=AuthState.phone, content_types=types.ContentType.TEXT)
async def login(message: types.Message, state=FSMContext):
    phone = message.text
    if phone:
        msg = await get_code(phone)
        if not msg[1]:         
            await message.answer(msg[0])
            return
    await message.answer(msg[0])
    await message.answer("Bot orqali yuborilgan kodni kiriting.")
    await AuthState.code.set()
    await state.update_data({
        "guid": msg[1]
    })
    

@dp.message_handler(state=AuthState.code, content_types=types.ContentType.TEXT)
async def login(message: types.Message, state=FSMContext):
    code = message.text
    data = await state.get_data()
    msg = await verify(code, data.get('guid'))
    await message.answer(msg)
    await state.finish()
    
    