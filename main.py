import httpx
from typing import Annotated
from datetime import date
from tools import group_tariff_by_date
from models import Cargo, Tariff
from fastapi import FastAPI, Form, Request
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

# TODO: create a data creation API
app = FastAPI(docs_url='/')
cargo_pydantic = pydantic_model_creator(Cargo)
tariff_pydantic = pydantic_model_creator(Tariff)


@app.get("/cargos")
async def get_cargos():
    """Get the list of existing cargos."""
    return await cargo_pydantic.from_queryset(Cargo.all())


@app.get("/tariff")
async def get_tariffs_by_date():
    """Gets tariff rates for each cargo by date."""
    tariff = Tariff.all().order_by("date")
    return await group_tariff_by_date(tariff)


@app.get("/get_insurance")
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


@app.get("/get_insurance/by_date")
async def calc_insurance_by_date(request: Request, cargo_name: str, cargo_price: int, cargo_date: date):
    """
    Given the cargo's name and price, calculates the insurance according to tariff for specific date.
    """
    insurances = await calc_insurance(request, cargo_name, cargo_price)
    if insurances and type(insurances) == dict:
        print("!!", {str(cargo_date): insurances['insurances'][str(cargo_date)]})
        return {
            'cargo': cargo_name,
            'price': cargo_price,
            'insurance': {str(cargo_date): insurances['insurances'][str(cargo_date)]}}
    return insurances


@app.post("/cargos/create")
async def say_hello(name=Form(...)):
    """Adds cargo to cargo list."""
    cargo = await Cargo.create(name=name)
    cargo_json = await cargo_pydantic.from_tortoise_orm(cargo)
    return cargo_json

register_tortoise(app, db_url='sqlite://database.sqlite3',
                  modules={"models": ['models']},
                  generate_schemas=True,
                  add_exception_handlers=True)