from database.session import session
from database.models import Products_type, Material_type

def calculate_material_quantity(product_type_id, material_type_id):
    type_coef = session.query(Products_type.type_coef).filter_by(id=product_type_id).scalar()
    material_defect = session.query(Material_type.defect_percent).filter_by(id=material_type_id).scalar()
    necessary_quantity = type_coef - (type_coef * material_defect)
    return round(necessary_quantity, 5)
