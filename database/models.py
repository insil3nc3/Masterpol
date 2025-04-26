from sqlalchemy import Column, Table, Integer, String, create_engine, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

Base = declarative_base()


class Partner_type(Base):
    __tablename__ = "partner_type"

    id = Column(Integer, primary_key=True)
    partner_type = Column(String, unique=True, nullable=False)

    partners = relationship("Partners", back_populates="partner_type")


class Partners(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True)
    partner_type_id = Column(Integer, ForeignKey("partner_type.id"))
    partner_name = Column(String)
    director = Column(String)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)
    INN = Column(String)
    rating = Column(Integer)

    partner_type = relationship("Partner_type", back_populates="partners")
    partner_products = relationship("Partner_products", back_populates="partner")

class Partner_products(Base):
    __tablename__ = "partner_products"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("products.article"))
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    product_quantity = Column(Integer)
    sale_data = Column(Date)

    partner = relationship("Partners", back_populates="partner_products")
    products = relationship("Products", back_populates="partner_products")

class Products(Base):
    __tablename__ = "products"

    article = Column(Integer, primary_key=True)
    product_type_id = Column(Integer, ForeignKey("products_type.id"))
    material_type_id = Column(Integer, ForeignKey("material_type.id"))
    product_name = Column(String)
    min_price_for_partner = Column(Integer)

    partner_products = relationship("Partner_products", back_populates="products")
    product_type = relationship("Products_type", back_populates="products")
    material_type = relationship("Material_type", back_populates="products")

class Products_type(Base):
    __tablename__ = "products_type"

    id = Column(Integer, primary_key=True)
    product_type = Column(String)
    type_coef = Column(Integer)

    products = relationship("Products", back_populates="product_type")

class Material_type(Base):
    __tablename__ = "material_type"

    id = Column(Integer, primary_key=True)
    material_type = Column(String)
    defect_percent = Column(Integer)

    products = relationship("Products", back_populates="material_type")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Partners.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Base.metadata.create_all(engine)
