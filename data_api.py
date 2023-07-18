from fastapi.routing import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi import Form
from models import Cargo
import create_data

router = APIRouter(prefix='/data', tags=['Data Manager'])
cargo_pydantic = pydantic_model_creator(Cargo)


@router.post("/tariff")
async def create_tariff(date_amount: int=5):
    """Creates default tariff plan.
    'date_amount' is the parameter that determines to how many days
    (starting from today) the tariff will include rates."""
    await create_data.create_tariffs(date_amount)
    return {'message': f'Successfully created {date_amount} day tariff!'}


@router.post("/cargos")
async def create_cargos():
    """Creates default list of Cargos"""
    await create_data.create_cargos()
    return {'message': f'Successfully created default cargo list!',
            'cargos': create_data.basic_cargos}


@router.post("/cargos/add")
async def add_cargo(name=Form(...)):
    """Adds cargo to cargo list."""
    cargo = await Cargo.create(name=name)
    cargo_json = await cargo_pydantic.from_tortoise_orm(cargo)
    return cargo_json


@router.delete("/tariff")
async def delete_tariff():
    """Deletes the Tariff."""
    await create_data.delete_tariffs()
    return {'message': 'Deleted  the Tariff.'}


@router.delete("/cargos")
async def delete_cargos():
    """Deletes all cargo instances."""
    await create_data.delete_cargos()
    return {'message': 'Deleted all Cargo instances.'}