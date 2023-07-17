from fastapi import FastAPI, Form, HTTPException
from models import Cargo
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

app = FastAPI()
cargo_pydantic = pydantic_model_creator(Cargo)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cargos", status_code=201)
async def get_cargos():
    return await cargo_pydantic.from_queryset(Cargo.all())


@app.get("/cargos/{cargo_id}", status_code=201, responses={
    404: {'model': HTTPNotFoundError}
})
async def get_cargos_by_id(cargo_id: int):
    return await cargo_pydantic.from_queryset_single(Cargo.get(pk=cargo_id))


@app.post("/cargos/create")
async def say_hello(rate: float, name=Form(...)):
    cargo = await Cargo.create(name=name, rate=rate)
    cargo_json = await cargo_pydantic.from_tortoise_orm(cargo)
    return cargo_json

register_tortoise(app, db_url='sqlite://database.sqlite3',
                  modules={"models": ['models']},
                  generate_schemas=True,
                  add_exception_handlers=True)