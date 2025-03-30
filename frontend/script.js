const apiUrl = 'https://ts.jijathecat.space/logistics/api';  // Бэкенд на сервере

// Ждем загрузки DOM перед выполнением
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");
    getClients();
    getRoutes();
    getWarehouses();  // Получаем список складов
    getOrders();  // Получаем список заказов
    showTab('clients');
});

// Переключение вкладок
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.getElementById(tabId).style.display = 'block';
}

// ===================== КЛИЕНТЫ =====================

// Создание клиента
document.getElementById('client-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    console.log("Отправка формы...");

    const clientName = document.getElementById('client-name').value;
    const clientEmail = document.getElementById('client-email').value;
    const clientPhone = document.getElementById('client-phone').value;

    const newClient = { name: clientName, email: clientEmail, phone: clientPhone };

    try {
        const response = await fetch(`${apiUrl}/clients/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newClient)
        });

        if (response.ok) {
            alert('Клиент создан!');
            getClients();
            document.getElementById('client-form').reset(); // Очищаем форму
        } else {
            alert('Ошибка при создании клиента');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});

// Получение списка клиентов
async function getClients() {
    try {
        const response = await fetch(`${apiUrl}/clients/`);
        const clients = await response.json();
        const clientList = document.getElementById('clients-list');
        const clientSelect = document.getElementById('order-client');
        clientList.innerHTML = '';
        clientSelect.innerHTML = '';  // Очищаем старые данные

        clients.forEach(client => {
            // Отображаем в списке клиентов
            const li = document.createElement('li');
            li.innerHTML = `Имя: ${client.name}, Email: ${client.email}, Телефон: ${client.phone}
                <button onclick="editClient(${client.id})">✏️</button>
                <button onclick="deleteClient(${client.id})">🗑️</button>`;
            clientList.appendChild(li);

            // Добавляем клиентов в выпадающий список для заказов
            const option = document.createElement('option');
            option.value = client.id;
            option.textContent = client.name;
            clientSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Редактирование клиента
async function editClient(clientId) {
    try {
        const response = await fetch(`${apiUrl}/clients/${clientId}`);
        const client = await response.json();

        console.log(`Выбрали клиента ID ${clientId} для редактирования`);

        document.getElementById('client-name').value = client.name;
        document.getElementById('client-email').value = client.email;
        document.getElementById('client-phone').value = client.phone;

        // Меняем кнопку на "Обновить"
        const submitButton = document.querySelector('#client-form button');
        submitButton.textContent = "Обновить клиента";
        submitButton.onclick = async (event) => {
            event.preventDefault();
            await updateClient(clientId);
        };

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Обновление клиента
async function updateClient(clientId) {
    const updatedClient = {
        name: document.getElementById('client-name').value,
        email: document.getElementById('client-email').value,
        phone: document.getElementById('client-phone').value
    };

    try {
        const response = await fetch(`${apiUrl}/clients/${clientId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedClient)
        });

        if (response.ok) {
            alert('Клиент обновлён!');
            getClients();
            document.getElementById('client-form').reset();
            document.querySelector('#client-form button').textContent = "Создать клиента";
        } else {
            alert('Ошибка при обновлении клиента');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Удаление клиента
async function deleteClient(clientId) {
    if (!confirm("Удалить клиента?")) return;

    try {
        const response = await fetch(`${apiUrl}/clients/${clientId}`, { method: 'DELETE' });

        if (response.ok) {
            alert('Клиент удалён!');
            getClients();
        } else {
            alert('Ошибка при удалении клиента');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// ===================== МАРШРУТЫ =====================

// Создание маршрута
document.getElementById('route-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    console.log("Отправка формы маршрута...");

    const routeOrigin = document.getElementById('route-origin').value;
    const routeDestination = document.getElementById('route-destination').value;
    const routeDistance = document.getElementById('route-distance').value;

    const newRoute = { origin: routeOrigin, destination: routeDestination, distance: routeDistance, };

    try {
        const response = await fetch(`${apiUrl}/routes/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newRoute)
        });

        if (response.ok) {
            alert('Маршрут создан!');
            getRoutes();
            document.getElementById('route-form').reset(); // Очищаем форму
        } else {
            alert('Ошибка при создании маршрута');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});

// Получение списка маршрутов
async function getRoutes() {
    try {
        const response = await fetch(`${apiUrl}/routes/`);
        const routes = await response.json();
        const routeList = document.getElementById('routes-list');
        const routeSelect = document.getElementById('order-route');
        routeList.innerHTML = '';
        routeSelect.innerHTML = '';  // Очищаем старые данные

        routes.forEach(route => {
            // Отображаем маршруты
            const li = document.createElement('li');
            li.innerHTML = `Маршрут: ${route.id}, Откуда: ${route.origin}, Куда: ${route.destination}, Расстояние: ${route.distance}
                <button onclick="editRoute(${route.id})">✏️</button>
                <button onclick="deleteRoute(${route.id})">🗑️</button>`;
            routeList.appendChild(li);

            // Добавляем маршруты в выпадающий список для заказов
            const option = document.createElement('option');
            option.value = route.id;
            option.textContent = `${route.origin} - ${route.destination}`;
            routeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Редактирование маршрута
async function editRoute(routeId) {
    try {
        const response = await fetch(`${apiUrl}/routes/${routeId}`);
        const route = await response.json();

        console.log(`Выбрали маршрут ID ${routeId} для редактирования`);

        document.getElementById('route-origin').value = route.origin;
        document.getElementById('route-destination').value = route.destination;
        document.getElementById('route-distance').value = route.distance;

        // Меняем кнопку на "Обновить"
        const submitButton = document.querySelector('#route-form button');
        submitButton.textContent = "Обновить маршрут";
        submitButton.onclick = async (event) => {
            event.preventDefault();
            await updateRoute(routeId);
        };

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Обновление маршрута
async function updateRoute(routeId) {
    const updatedRoute = {
        origin: document.getElementById('route-origin').value,
        destination: document.getElementById('route-destination').value,
        distance: document.getElementById('route-distance').value
    };

    try {
        const response = await fetch(`${apiUrl}/routes/${routeId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedRoute)
        });

        if (response.ok) {
            alert('Маршрут обновлён!');
            getRoutes();
            document.getElementById('route-form').reset();
            document.querySelector('#route-form button').textContent = "Создать маршрут";
        } else {
            alert('Ошибка при обновлении маршрута');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Удаление маршрута
async function deleteRoute(routeId) {
    if (!confirm("Удалить маршрут?")) return;

    try {
        const response = await fetch(`${apiUrl}/routes/${routeId}`, { method: 'DELETE' });

        if (response.ok) {
            alert('Маршрут удалён!');
            getRoutes();
        } else {
            alert('Ошибка при удалении маршрута');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// ===================== ЗАКАЗЫ =====================

// Получение списка заказов
async function getOrders() {
    try {
        const response = await fetch(`${apiUrl}/orders/`);
        const orders = await response.json();
        const orderList = document.getElementById('orders-list');
        orderList.innerHTML = '';

        orders.forEach(order => {
            if (order.client && order.client.name) {
                const li = document.createElement('li');
                li.innerHTML = `Заказ ${order.id}: Груз: ${order.cargo}, Клиент: ${order.client.name}, Маршрут: ${order.route.origin} - ${order.route.destination}, Склад: ${order.warehouse.name}
                    <button onclick="editOrder(${order.id})">✏️</button>
                    <button onclick="deleteOrder(${order.id})">🗑️</button>`;
                orderList.appendChild(li);
            }
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Создание нового заказа
document.getElementById('order-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    console.log("Отправка формы заказа...");

    const clientId = document.getElementById('order-client').value;
    const cargo = document.getElementById('order-cargo').value;
    const routeId = document.getElementById('order-route').value;
    const warehouseId = document.getElementById('order-warehouse').value;

    const newOrder = { client_id: clientId, cargo: cargo, route_id: routeId, warehouse_id: warehouseId };

    try {
        const response = await fetch(`${apiUrl}/orders/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        });

        if (response.ok) {
            alert('Заказ создан!');
            getOrders();
            document.getElementById('order-form').reset(); // Очищаем форму
        } else {
            alert('Ошибка при создании заказа');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});