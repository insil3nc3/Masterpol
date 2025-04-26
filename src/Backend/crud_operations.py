from logging import exception

from sqlalchemy.exc import SQLAlchemyError

from database.session import session
from database.models import Partner_products, Partners, Partner_type, Products


def get_partner_type_id_by_name(p_type: str) -> int:
    """Возвращает ID типа партнёра по его названию."""
    typo = session.query(Partner_type).filter_by(partner_type=p_type).first()
    if typo:
        return typo.id
    raise ValueError(f"Тип партнера '{p_type}' не найден")


def get_partner_types():
    types = session.query(Partner_type.partner_type).all()
    return[typo[0] for typo in types]

def add_partner(p_type, p_name, director, email, phone_number, address, INN, rating):

    p_type_id = get_partner_type_id_by_name(p_type)
    try:
        data = Partners(partner_type_id=p_type_id,
                        partner_name=p_name,
                        director=director,
                        email=email,
                        phone_number=phone_number,
                        address=address,
                        INN=INN,
                        rating=rating)
        session.add(data)
        session.commit()
        return 0
    except SQLAlchemyError as e:
        session.rollback()
        return -1
    except exception as e:
        session.rollback()
        return -2

def delete_partner(p_id: int):
    partner = get_partner_by_id(p_id)
    if partner:
        session.delete(partner)
        session.commit()
    else:
        print(f"партнер с айди {p_id} не найден в базе")

def get_partner_by_id(p_id):
    partner = session.query(Partners).filter_by(id=p_id).first()
    return partner

def get_partner_by_name(p_name):
    partner = session.query(Partners).filter_by(partner_name=p_name).first()
    return partner

def delete_partner(p_id):
    partner = session.get(Partners, p_id)
    if not partner:
        return -1
    session.delete(partner)
    session.commit()
    return True

def edit_partner(p_id, p_type, p_name, director, email, phone_number, address, INN, rating):
    p_type_id = get_partner_type_id_by_name(p_type)
    partner = session.query(Partners).filter_by(id = p_id).first()
    try:
        partner.partner_type_id = p_type_id
        partner.partner_name = p_name
        partner.director = director
        partner.email = email
        partner.phone_number = phone_number
        partner.address = address
        partner.INN = INN
        partner.rating = rating
        session.commit()
        return 0
    except SQLAlchemyError as e:
        print("ОШИБКА:", e)
        return -1
    except exception as e:
        return -2

def get_product_quantity(p_name):
    partner = get_partner_by_name(p_name)
    p_id = partner.id
    product_quantity = session.query(Partner_products).filter_by(partner_id=p_id).count()
    return product_quantity

def history_query(p_name):
    partner = get_partner_by_name(p_name)
    p_id = partner.id
    p_products = session.query(Partner_products).filter_by(partner_id=p_id).all()
    data = {}
    for p_product in p_products:
        product_name = session.query(Products).filter_by(article=p_product.product_id).first()
        data[p_products.index(p_product)] = {"product_name":product_name.product_name,
                              "product_quantity":p_product.product_quantity,
                              "data":p_product.sale_data.strftime("%Y-%m-%d")}
    return data

