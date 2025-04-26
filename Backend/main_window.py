from database.session import session
from database.models import Partner_products, Partners, Partner_type


def calculate_discount(partner_id):
    products = session.query(Partner_products).filter_by(partner_id=partner_id).all()
    total_quantity_sold = 0
    for product in products:
        total_quantity_sold += product.product_quantity
    if total_quantity_sold <= 10000:
        discount = 0
    elif 10000 < total_quantity_sold <= 50000:
        discount = 5
    elif 50000 < total_quantity_sold <= 300000:
        discount = 10
    else:
        discount = 15

    return discount

def partners_info(partner_id):
    partner = session.query(Partners).filter_by(id=partner_id).first()
    if partner:
        partner_type = session.query(Partner_type.partner_type).filter_by(id=partner.partner_type_id).scalar()

        return {"partner_type":partner_type,
                "partner_name":partner.partner_name,
                "discount":calculate_discount(partner_id),
                "director":partner.director,
                "phone":partner.phone_number,
                "rating":partner.rating}
    else:
        return -1

def get_partners_quantity():
    """Возвращает ID последней записи в таблице Partners"""
    last_partner = session.query(Partners).order_by(Partners.id.desc()).first()
    if last_partner:
        return last_partner.id
    return None  # или 0, если таблица пуста

