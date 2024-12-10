from fastapi import APIRouter, HTTPException, Depends
import pigpio
import time 
import threading
from datetime import datetime
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.NumberPlateModel import NumberPlates
from sqlalchemy import update, insert, select, cast, exc
from config import CONTROL_GPIO, OPEN_DURATION


if CONTROL_GPIO < 0 or CONTROL_GPIO > 40:
    print("Invalid GPIO number!")
    exit()


pi = pigpio.pi()
pi.set_mode(CONTROL_GPIO, pigpio.OUTPUT)
pi.write(CONTROL_GPIO, 0)

def open_timed(time_sec):
    pi.write(CONTROL_GPIO, 1)
    time.sleep(time_sec)
    pi.write(CONTROL_GPIO, 0)
    return

def request_open():
    global switch_thread
    if not switch_thread.is_alive():
        switch_thread = threading.Thread(target=open_timed, args=(OPEN_DURATION,))
        switch_thread.start()

switch_thread = threading.Thread(target=open_timed, args=(OPEN_DURATION,))

request_router = APIRouter(
    prefix="/api/v1/request",
    tags=["Req"]
)

#Запрос на открытие с валидацией через БД
@request_router.get("/validate_open/{numberPlate_str}")
async def get_user(numberPlate_str: str, session: AsyncSession = Depends(get_async_session)):

    try:
        req = await session.execute(select(NumberPlates).where(NumberPlates.number_plate == str(numberPlate_str)))
        numberPlate = req.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Нет информации по номеру")

    if numberPlate is not None:
        if(numberPlate.valid_until == None):
            request_open()
            return True
        validDate = numberPlate.valid_until.strftime("%Y-%m-%d")
        curDate = datetime.today().strftime("%Y-%m-%d")
        if(validDate >= curDate):
            request_open()
            return True
        else:
            raise HTTPException(status_code=404, detail="Срок пропуска истёк")
    return False

    

#Запрос на открытие с использованием ключа
@request_router.get("/key_open/{key}")
async def get_user(key):
    return key
    
