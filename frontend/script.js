const apiUrl = 'https://ts.jijathecat.space/logistics/api';  // Бэкенд на сервере

// Ждем загрузки DOM перед выполнением
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");

    const token = localStorage.getItem('token');

    // Проверяем, если нет токена, перенаправляем на страницу логина
    if (!token) {
        alert('Пожалуйста, войдите в систему');
        window.location.href = 'login.html'; // Перенаправляем на страницу входа
    }

    showTab('clients-tab');
    getClients();
    getRoutes();
    getWarehouses();  // Получаем список складов
    getOrders();  // Получаем список заказов
    showTab('clients');
});

// Переключение вкладок
function showTab(tabId) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.add('active');
    }
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

        // Проверка, существует ли элемент с id 'clients-list'
        if (!clientList) {
            console.error('Элемент с id "clients-list" не найден.');
            return;
        }

        const clientSelect = document.getElementById('order-client');
        clientList.innerHTML = ''; // Очищаем список
//        clientSelect.innerHTML = '';  // Очищаем старые данные

        clients.forEach(client => {
            // Отображаем в списке клиентов
            const li = document.createElement('li');
            li.innerHTML = `Имя: ${client.name}, Email: ${client.email}, Телефон: ${client.phone}
                <button onclick="editClient(${client.id})">✏️</button>
                <button onclick="deleteClient(${client.id})">🗑️</button>`;
            clientList.appendChild(li);

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
//async function getOrders() {
//    try {
//        const response = await fetch(`${apiUrl}/orders/`);
//        const orders = await response.json();
//        const orderList = document.getElementById('orders-list');
//        orderList.innerHTML = '';  // Очищаем список перед добавлением новых данных
//
//        for (let order of orders) {
//            const li = document.createElement('li');
//            li.innerHTML = `Заказ: ${order.order_id}, Клиент: ${order.client_name}, Маршрут: ${order.origin} - ${order.destination}, Склад: ${order.warehouse_name}, Статус: ${order.order_status}
//                <button onclick="editOrder(${order.order_id})">✏️</button>
//                <button onclick="deleteOrder(${order.order_id})">🗑️</button>`;
//            orderList.appendChild(li);
//        }
//    } catch (error) {
//        console.error('Ошибка:', error);
//    }
//}
//// ===================== ЗАКАЗЫ =====================
//
//// Создание нового заказа
//document.getElementById('order-form').addEventListener('submit', async (event) => {
//    event.preventDefault();
//    console.log("Отправка формы заказа...");
//
//    const clientName = document.getElementById('order-client-name').value;
//    const clientEmail = document.getElementById('order-client-email').value;
//    const clientPhone = document.getElementById('order-client-phone').value;
//
//    const cargoDescription = document.getElementById('cargo-input').value;
//    const cargoWeight = document.getElementById('cargo-weight').value;
//    const cargoVolume = document.getElementById('cargo-volume').value;
//
//    const routeId = document.getElementById('order-route').value;
//    const warehouseId = document.getElementById('order-warehouse').value;
//
//    const newOrder = {
//    client_name: clientName,
//    client_email: clientEmail,
//    client_phone: clientPhone,
//    cargo_description: cargoDescription,
//    cargo_weight: cargoWeight,
//    cargo_volume: cargoVolume,
//    route_id: routeId,
//    warehouse_id: warehouseId
//    };
//
//    try {
//        const response = await fetch(`${apiUrl}/orders/create-full`, {
//            method: 'POST',
//            headers: { 'Content-Type': 'application/json' },
//            body: JSON.stringify(newOrder)
//        });
//
//        if (response.ok) {
//            alert('Заказ создан!');
//            getOrders();  // Обновляем список заказов
//            document.getElementById('order-form').reset(); // Очищаем форму
//        } else {
//            alert('Ошибка при создании заказа');
//        }
//    } catch (error) {
//        console.error('Ошибка:', error);
//    }
//});

// Редактирование заказа
async function editOrder(orderId) {
    try {
        const response = await fetch(`${apiUrl}/orders/${orderId}`);
        const order = await response.json();

        console.log(`Выбрали заказ ID ${orderId} для редактирования`);

        document.getElementById('order-client-name').value = order.client_name;
        document.getElementById('order-client-email').value = order.client_email;
        document.getElementById('order-client-phone').value = order.client_phone;
        document.getElementById('cargo-input').value = order.cargo_description;
        document.getElementById('cargo-weight').value = order.cargo_weight;
        document.getElementById('cargo-volume').value = order.cargo_volume;
        document.getElementById('order-route').value = order.route_id;
        document.getElementById('order-warehouse').value = order.warehouse_id;

        // Меняем кнопку на "Обновить"
        const submitButton = document.querySelector('#order-form button');
        submitButton.textContent = "Обновить заказ";
        submitButton.onclick = async (event) => {
            event.preventDefault();
            await updateOrder(orderId);
        };

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Обновление заказа
async function updateOrder(orderId) {
    const updatedOrder = {
        client_name: document.getElementById('order-client-name').value,
        client_email: document.getElementById('order-client-email').value,
        client_phone: document.getElementById('order-client-phone').value,
        cargo_description: document.getElementById('cargo-input').value,
        cargo_weight: document.getElementById('cargo-weight').value,
        cargo_volume: document.getElementById('cargo-volume').value,
        route_id: document.getElementById('order-route').value,
        warehouse_id: document.getElementById('order-warehouse').value
    };

    try {
        const response = await fetch(`${apiUrl}/orders/${orderId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedOrder)
        });

        if (response.ok) {
            alert('Заказ обновлён!');
            getOrders(); // Обновляем список заказов
            document.getElementById('order-form').reset(); // Очищаем форму
            document.querySelector('#order-form button').textContent = "Создать заказ"; // Меняем текст кнопки
        } else {
            alert('Ошибка при обновлении заказа');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}


function checkAndAddOption(selectId) {
    const selectElement = document.getElementById(selectId);
    const inputElement = document.getElementById(selectId + '-input');
    const inputValue = inputElement.value.trim();

    if (inputValue && !Array.from(selectElement.options).some(option => option.value === inputValue)) {
        // Если введено значение и оно не существует в выпадающем списке
        const newOption = document.createElement('option');
        newOption.value = inputValue;
        newOption.text = inputValue;
        selectElement.appendChild(newOption);
    }
}

// Функция для добавления нового клиента или груза в выпадающий список
function addNewOption(selectId, inputId) {
    const inputValue = document.getElementById(inputId).value.trim();
    const selectElement = document.getElementById(selectId);

    if (inputValue && !Array.from(selectElement.options).some(option => option.value === inputValue)) {
        const newOption = document.createElement('option');
        newOption.value = inputValue;
        newOption.text = inputValue;
        selectElement.appendChild(newOption);
    }
}


// ===================== СКЛАДЫ =====================

// Получение списка складов
async function getWarehouses() {
    try {
        const response = await fetch(`${apiUrl}/warehouses/`);
        const warehouses = await response.json();
        const warehouseSelect = document.getElementById('order-warehouse');
        warehouseSelect.innerHTML = '';  // Очищаем старые данные

        warehouses.forEach(warehouse => {
            const option = document.createElement('option');
            option.value = warehouse.id;
            option.textContent = warehouse.name;
            warehouseSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка при получении складов:', error);
    }
}

async function getOrders() {
    const clientName = document.getElementById('filter-client-name').value.trim();
    const clientEmail = document.getElementById('filter-client-email').value.trim();
    const warehouseName = document.getElementById('filter-warehouse-name').value.trim();
    const warehouseLocation = document.getElementById('filter-warehouse-location').value.trim();

    let filterParams = {};

    if (clientName) filterParams.client_name = clientName;
    if (clientEmail) filterParams.client_email = clientEmail;
    if (warehouseName) filterParams.warehouse_name = warehouseName;
    if (warehouseLocation) filterParams.warehouse_location = warehouseLocation;

    const queryString = new URLSearchParams(filterParams).toString();
    const url = `${apiUrl}/orders/filter/` + (queryString ? '?' + queryString : '');

    try {
        const response = await fetch(url);
        const orders = await response.json();
        const orderList = document.getElementById('orders-list');
        orderList.innerHTML = '';  // Очищаем список перед добавлением новых данных

        for (let order of orders) {
            const li = document.createElement('li');
            li.innerHTML = `Заказ: ${order.order_id}, Клиент: ${order.client_name}, Маршрут: ${order.origin} - ${order.destination}, Склад: ${order.warehouse_name}, Статус: ${order.order_status}
                <button onclick="editOrder(${order.order_id})">✏️</button>
                <button onclick="deleteOrder(${order.order_id})">🗑️</button>`;
            orderList.appendChild(li);
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Функция для создания нового заказа
document.getElementById('order-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    console.log("Отправка формы заказа...");

    const clientName = document.getElementById('order-client-name').value;
    const clientEmail = document.getElementById('order-client-email').value;
    const clientPhone = document.getElementById('order-client-phone').value;

    const cargoDescription = document.getElementById('cargo-input').value;
    const cargoWeight = document.getElementById('cargo-weight').value;
    const cargoVolume = document.getElementById('cargo-volume').value;

    const routeId = document.getElementById('order-route').value;
    const warehouseId = document.getElementById('order-warehouse').value;

    const newOrder = {
        client_name: clientName,
        client_email: clientEmail,
        client_phone: clientPhone,
        cargo_description: cargoDescription,
        cargo_weight: cargoWeight,
        cargo_volume: cargoVolume,
        route_id: routeId,
        warehouse_id: warehouseId
    };

    try {
        const response = await fetch(`${apiUrl}/orders/create-full`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        });

        if (response.ok) {
            alert('Заказ создан!');
            getOrders();  // Обновляем список заказов
            document.getElementById('order-form').reset(); // Очищаем форму
        } else {
            alert('Ошибка при создании заказа');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});