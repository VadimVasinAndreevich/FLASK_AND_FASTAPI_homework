"""
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц:
товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля:
id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля:
id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
"""

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List
from fastapi.responses import HTMLResponse
from random import uniform, randint
import datetime

DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(64)),
    )


products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name_prod", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("price", sqlalchemy.Float),
    )


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("id_product", sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(128)),
    )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
    )

metadata.create_all(engine)

app = FastAPI()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: EmailStr
    password: str = Field(max_length=64)


class ProductIn(BaseModel):
    name_prod: str = Field(max_length=32)
    description: str = Field(max_length=1000)
    price: float


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: str = Field(max_length=32)
    status: str = Field(max_length=128)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: EmailStr
    password: SecretStr


class Product(BaseModel):
    id: int
    name_prod: str = Field(max_length=32)
    description: str = Field(max_length=1000)
    price: float


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: str = Field(max_length=32)
    status: str = Field(max_length=128)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/', response_class=HTMLResponse)
async def line():
    return "<a href='/docs'>.....Автодок.....</a>"


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/fake_users/{count}")
async def create_user_fake(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}', surname=f'userstar{i}', email=f'mail{i}@mail.ru',
                                      password=f'Fa{i+21-132-56+1015}kE_Pas{i+2}#sWo${i-100}rd@#{i+i*i}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.get("/fake_products/{count}")
async def create_prod(count: int):
    for i in range(count):
        query = products.insert().values(name_prod=f'object_{i}', description=f'quality_{i}',
                                         price=round(uniform(0.01, 10.01), 2))
        await database.execute(query)
    return {'message': f'{count} fake products create'}


@app.get("/fake_orders/{count}")
async def create_order_fake(skip: int, limit: int):
    for i in range(skip, limit+1):
        count_prod = randint(1, 3)
        for prod in range(count_prod):
            query = orders.insert().values(id_user=i, id_product=randint(0, 50), date=datetime.datetime.now(),
                                          status='создан, ожидает обработки')
            await database.execute(query)
    return {'message': f'for {limit-skip} fake users create fake orders'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(id_user=order.user_id, id_product=order.product_id, date=datetime.datetime.now(),
                                   status='создан, ожидает обработки')
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name_prod=product.name_prod, description=product.description, price=product.price)
    query = products.insert().values(**product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**user.dict())
    await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await database.execute(query)
    return {**product.dict(), "id": product_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**order.dict())
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@app.delete("/users/{user_id}")
async def delete_user(skip: int, limit: int):
    for i in range(skip, limit+1):
        query = users.delete().where(users.c.id == i)
        await database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/products/{product_id}")
async def delete_product(skip: int, limit: int):
    for i in range(skip, limit+1):
        query = products.delete().where(products.c.id == i)
        await database.execute(query)
    return {'message': 'Product deleted'}


@app.delete("/orders/{order_id}")
async def delete_product(skip: int, limit: int):
    for i in range(skip, limit+1):
        query = orders.delete().where(orders.c.id == i)
        await database.execute(query)
    return {'message': 'Order deleted'}
