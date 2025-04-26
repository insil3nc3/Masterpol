import pandas as pd
from sqlalchemy.orm import sessionmaker
from database.models import Partners, Products, Partner_products, Partner_type, Products_type, Material_type
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("sqlite:///Partners.db")
Session = sessionmaker(engine)
session = Session()

def insert_partner_type():
    df = pd.read_excel("../src/Partners_import.xlsx")

    unique_partner_types = df["Тип партнера"].unique()

    for partner_type in unique_partner_types:

        exists = session.query(Partner_type).filter_by(partner_type=partner_type).first()
        if not exists:
            data = Partner_type(partner_type=partner_type)
            session.add(data)

    session.commit()

def insert_partners():
    df = pd.read_excel("../src/Partners_import.xlsx")
    for _, row in df.iterrows():
        partner_type = row["Тип партнера"]
        partner_name = row["Наименование партнера"]
        director = row["Директор"]
        email = row["Электронная почта партнера"]
        phone_number = row["Телефон партнера"]
        address = row["Юридический адрес партнера"]
        INN = row["ИНН"]
        rating = row["Рейтинг"]

        partner = session.query(Partner_type).filter_by(partner_type=partner_type).first()
        partner_type_id = partner.id

        data = Partners(
            partner_type_id=partner_type_id,
            partner_name=partner_name,
            director=director,
            email=email,
            phone_number=phone_number,
            address=address,
            INN=INN,
            rating=rating
        )
        session.add(data)
    session.commit()

def insert_products_type():
    df = pd.read_excel("../src/Product_type_import.xlsx")

    for _, row in df.iterrows():
        product_type = row["Тип продукции"]
        type_coef = row["Коэффициент типа продукции"]


        exists = session.query(Products_type).filter_by(product_type=product_type).first()
        if not exists:
            data = Products_type(
                product_type=product_type,
                type_coef=type_coef
            )
            session.add(data)
    session.commit()

def insert_material_type():
    df = pd.read_excel("../src/Material_type_import.xlsx")

    for _, row in df.iterrows():
        mat_type = row["Тип материала"]
        defect_percent = row["Процент брака материала "]

        exists = session.query(Material_type).filter_by(material_type=mat_type).first()
        if not exists:
            data = Material_type(
                material_type=mat_type,
                defect_percent=defect_percent
            )
            session.add(data)
    session.commit()

def insert_products():
    df = pd.read_excel("../src/Products_import.xlsx")

    for _, row in df.iterrows():
        article = row["Артикул"]
        product_type = row["Тип продукции"]
        product_name = row["Наименование продукции"]
        min_price_for_partner = row["Минимальная стоимость для партнера"]


        product_type_obj = session.query(Products_type).filter_by(product_type=product_type).first()

        exists = session.query(Products).filter_by(article=article).first()
        if not exists:
            data = Products(
                article=article,
                product_type_id=product_type_obj.id,
                product_name=product_name,
                min_price_for_partner=min_price_for_partner
            )
            session.add(data)
    session.commit()


def insert_partner_products():
    df = pd.read_excel("../src/Partner_products_import.xlsx")

    for _, row in df.iterrows():
        product_name = row["Продукция"]
        partner_name = row["Наименование партнера"]
        product_quantity = row["Количество продукции"]
        sale_date = row["Дата продажи"]

        product = session.query(Products).filter_by(product_name=product_name).first()
        product_id = product.article
        partner = session.query(Partners).filter_by(partner_name=partner_name).first()
        partner_id = partner.id
        data = Partner_products(
            product_id=product_id,
            partner_id=partner_id,
            product_quantity=product_quantity,
            sale_data=pd.to_datetime(sale_date).date()
        )
        session.add(data)
    session.commit()

# insert_partner_type()
# insert_material_type()
# insert_products_type()
# insert_partners()
# insert_products()
# insert_partner_products()