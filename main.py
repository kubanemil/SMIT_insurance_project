import httpx
import data_api
from datetime import date
from tools import group_tariff_by_date
from models import Cargo, Tariff
from fastapi import FastAPI, Request
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(docs_url='/')
app.include_router(data_api.router)

tariff_pydantic = pydantic_model_creator(Tariff)
cargo_pydantic = pydantic_model_creator(Cargo)

@app.get("/cargos", tags=['Main'])
async def get_cargos():
    """Get the list of existing cargos."""
    return await cargo_pydantic.from_queryset(Cargo.all())


@app.get("/tariff", tags=['Main'])
async def get_tariff():
    """Gets tariff rates for each cargo by date."""
    tariff = Tariff.all().order_by("date")
    return await group_tariff_by_date(tariff)


@app.get("/get_insurance", tags=['Main'])
async def calc_insurance(request: Request, cargo_name: str, cargo_price: int):
    """
    Given the cargo's name and price, calculates the insurance for each date according to tariff.
    """
    if await Cargo.filter(name=cargo_name).exists():
        # gets request with httpx in case that API is not internal.
        url_components = request.url.components
        tariff_url = f"{url_components[0]}://{url_components[1]}/tariff"
        async with httpx.AsyncClient() as client:
            response = await client.get(tariff_url)

        if response.status_code == 200:
            tariff = response.json()
            insurances = {}
            for day, infos in tariff.items():
                for info in infos:
                    if info['cargo_type'] == cargo_name:
                        insurances[day] = round(info['rate']*cargo_price, 5)
            return {
                'cargo': cargo_name,
                'price': cargo_price,
                'insurances': insurances}

        return {
            'message': 'Error with getting tariff.',
            'url': tariff_url,
            'status': response.status_code}

    return {'message': 'No specified cargo.'}


@app.get("/get_insurance/by_date", tags=['Main'])
async def calc_insurance_by_date(request: Request, cargo_name: str, cargo_price: int, cargo_date: date):
    """
    Given the cargo's name and price, calculates the insurance according to tariff for specific date.
    """
    response = await calc_insurance(request, cargo_name, cargo_price)
    insurances = response.get('insurances')
    if insurances and type(insurances) == dict:
        cargo_date = str(cargo_date)
        if insurances.get(cargo_date):
            return {
                'cargo': cargo_name,
                'price': cargo_price,
                'insurance': {cargo_date: insurances.get(cargo_date)}}
        return {'message': "No insurance record for a given date."}
    return response


register_tortoise(app, db_url='sqlite://database.sqlite3',
                  modules={"models": ['models']},
                  generate_schemas=True,
                  add_exception_handlers=True)