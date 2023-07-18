from fastapi import FastAPI, Form, Request
from models import Cargo, Tariff
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
import httpx

# TODO: create a data creation API
app = FastAPI()
cargo_pydantic = pydantic_model_creator(Cargo)
tariff_pydantic = pydantic_model_creator(Tariff)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tariffs", response_model=tariff_pydantic)
async def get_tariffs():
    return await tariff_pydantic.from_queryset(Tariff.all())


@app.get("/tariffs/date")
async def get_tariffs_by_date():
    tariffs = Tariff.all().order_by("date")

    grouped_data = {}
    async for item in tariffs:
        date = item.date.isoformat()
        type_rate = {
            'cargo_type': item.cargo_type,
            'rate': item.rate
        }
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append(type_rate)
    return grouped_data


@app.get("/insurance")
async def calc_insurance(request: Request, price: int, cargo: str):
    if await Cargo.filter(name=cargo).exists():
        url_components = request.url.components
        tariff_url = f"{url_components[0]}://{url_components[1]}/tariffs/date"
        async with httpx.AsyncClient() as client:
            response = await client.get(tariff_url)

        if response.status_code == 200:
            tariff = response.json()
            insurance = {}
            for date, infos in tariff.items():
                for info in infos:
                    if info['cargo_type'] == cargo:
                        insurance[date] = round(info['rate']*price, 5)
            return insurance
        return {'url': tariff_url,
                'status': response.status_code}
    return {'message': 'No specified cargo'}


@app.get("/cargos")
async def get_cargos():
    return await cargo_pydantic.from_queryset(Cargo.all())


@app.get("/cargos/{cargo_id}", responses={
    404: {'model': HTTPNotFoundError}
})
async def get_cargos_by_id(cargo_id: int):
    return await cargo_pydantic.from_queryset_single(Cargo.get(pk=cargo_id))


@app.post("/cargos/create")
async def say_hello(name=Form(...)):
    cargo = await Cargo.create(name=name)
    cargo_json = await cargo_pydantic.from_tortoise_orm(cargo)
    return cargo_json

register_tortoise(app, db_url='sqlite://database.sqlite3',
                  modules={"models": ['models']},
                  generate_schemas=True,
                  add_exception_handlers=True)