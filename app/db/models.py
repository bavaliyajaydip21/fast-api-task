from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import MetaData, Column, String, Integer, ForeignKey, Enum as SEnum
import enum


metadata = MetaData()
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    first_name = Column("first_name", String, nullable=True)
    last_name = Column("last_name", String, nullable=True)
    contact_info = Column("contact_info", String, nullable=True)
    status = Column("status", String, nullable=True)

    department_id = Column(Integer, ForeignKey("department.id"))
    position_id = Column(Integer, ForeignKey("position.id"))
    location_id = Column(Integer, ForeignKey("location.id"))
    company_id = Column(Integer, ForeignKey("company.id"))

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    location = relationship("Location", back_populates="employees")
    company = relationship("Company", back_populates="employees")


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    dynamic_columns = relationship("DynamicColumn", back_populates="company")
    employees = relationship("Employee", back_populates="company")
    departments = relationship("Department", back_populates="company")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="location")


class Position(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="position")


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department")


class DynamicColumn(Base):
    __tablename__ = "dynamic_column"

    id = Column(Integer, primary_key=True)
    fields = Column("fields", String, nullable=True)
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="dynamic_columns")
