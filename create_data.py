from random import randint
from models import Tariff, Cargo
from tortoise import Tortoise, run_async
from datetime import datetime, timedelta


basic_cargos = ['Glass', 'Plastic', 'Steel', 'Sugar', 'Wine']


async def connect_db():
    await Tortoise.init(
            db_url='sqlite://database.sqlite3',
            modules={'models': ['__main__']}
        )
    await Tortoise.generate_schemas()


async def create_tariffs():
    cargos = await Cargo.all()
    days = [datetime.today()+timedelta(days=i) for i in range(1, 6)]
    for day in days:
        for cargo in cargos:
            rate = randint(5, 100)/1000
            instance = Tariff(cargo_type=cargo.name, rate=rate, date=day)
            await instance.save()

    await Tortoise.close_connections()


async def create_cargos():
    for cargo in basic_cargos:
        cargo = Cargo(name=cargo)
        await cargo.save()


async def delete_cargos():
    await Cargo.all().delete()


async def delete_tariffs():
    await Tariff.all().delete()

if __name__ == '__main__':
    run_async(connect_db())
    run_async(create_cargos())
    run_async(create_tariffs())
