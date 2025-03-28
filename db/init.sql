-- Создаем таблицу статусов заказов, она будет ссылаться на себя
CREATE TABLE order_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Создаем таблицу клиентов
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15)
);

-- Создаем таблицу грузов
CREATE TABLE cargo (
    id SERIAL PRIMARY KEY,
    description TEXT,
    weight DECIMAL(10, 2),
    volume DECIMAL(10, 2)
);

-- Создаем таблицу складов
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(255)
);

-- Создаем таблицу маршрутов
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    distance DECIMAL(10, 2)
);

-- Создаем таблицу транспортных средств
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    license_plate VARCHAR(20),
    model VARCHAR(50)
);

-- Создаем таблицу водителей
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    license_number VARCHAR(20)
);

-- Создаем таблицу заказов, ссылаясь на order_statuses и другие таблицы
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id) ON DELETE CASCADE,
    cargo_id INT REFERENCES cargo(id) ON DELETE CASCADE,
    warehouse_id INT REFERENCES warehouses(id) ON DELETE SET NULL,
    route_id INT REFERENCES routes(id) ON DELETE CASCADE,
    status_id INT REFERENCES order_statuses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем таблицу назначений заказов
CREATE TABLE order_assignments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    driver_id INT REFERENCES drivers(id) ON DELETE CASCADE,
    vehicle_id INT REFERENCES vehicles(id) ON DELETE CASCADE,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP
);

-- Создаем таблицу движения груза
CREATE TABLE cargo_movements (
    id SERIAL PRIMARY KEY,
    cargo_id INT REFERENCES cargo(id) ON DELETE CASCADE,
    warehouse_id INT REFERENCES warehouses(id) ON DELETE CASCADE,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем таблицу оплаты заказов
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
