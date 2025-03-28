# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class OrderStatus(Base):
    __tablename__ = 'order_statuses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    # Связь с заказами
    orders = relationship("Order", back_populates="status")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(15))

    # Связь с заказами
    orders = relationship("Order", back_populates="client")


class Cargo(Base):
    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    weight = Column(DECIMAL(10, 2))
    volume = Column(DECIMAL(10, 2))

    # Связь с заказами
    orders = relationship("Order", back_populates="cargo")


class Warehouse(Base):
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(String(255))

    # Связь с движением грузов
    cargo_movements = relationship("CargoMovement", back_populates="warehouse")


class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(100))
    destination = Column(String(100))
    distance = Column(DECIMAL(10, 2))

    # Связь с заказами
    orders = relationship("Order", back_populates="route")


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(20))
    model = Column(String(50))

    # Связь с назначениями заказов
    assignments = relationship("OrderAssignment", back_populates="vehicle")


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    license_number = Column(String(20))

    # Связь с назначениями заказов
    assignments = relationship("OrderAssignment", back_populates="driver")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    cargo_id = Column(Integer, ForeignKey('cargo.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=True)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('order_statuses.id'), nullable=False)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

    # Связи с другими моделями
    client = relationship("Client", back_populates="orders")
    cargo = relationship("Cargo", back_populates="orders")
    warehouse = relationship("Warehouse", back_populates="cargo_movements")
    route = relationship("Route", back_populates="orders")
    status = relationship("OrderStatus", back_populates="orders")

    # Связь с назначениями заказов
    assignments = relationship("OrderAssignment", back_populates="order")

    # Связь с оплатами
    payments = relationship("Payment", back_populates="order")


class OrderAssignment(Base):
    __tablename__ = 'order_assignments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    start_date = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    end_date = Column(TIMESTAMP)

    # Связи с другими моделями
    order = relationship("Order", back_populates="assignments")
    driver = relationship("Driver", back_populates="assignments")
    vehicle = relationship("Vehicle", back_populates="assignments")


class CargoMovement(Base):
    __tablename__ = 'cargo_movements'

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(Integer, ForeignKey('cargo.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    movement_date = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

    # Связи с другими моделями
    cargo = relationship("Cargo", back_populates="cargo_movements")
    warehouse = relationship("Warehouse", back_populates="cargo_movements")


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_date = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

    # Связь с заказами
    order = relationship("Order", back_populates="payments")
