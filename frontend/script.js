const apiUrl = 'https://ts.jijathecat.space/logistics/api';  // Бэкенд на сервере

// Ждем загрузки DOM перед выполнением
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");
    getClients();
    getRoutes(); // Добавляем загрузку маршрутов
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
        clientList.innerHTML = '';

        clients.forEach(client => {
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

    const routeName = document.getElementById('route-name').value;
    const routeOrigin = document.getElementById('route-origin').value;
    const routeDestination = document.getElementById('route-destination').value;

    const newRoute = { name: routeName, origin: routeOrigin, destination: routeDestination };

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
        routeList.innerHTML = '';

        routes.forEach(route => {
            const li = document.createElement('li');
            li.innerHTML = `Маршрут: ${route.name}, Откуда: ${route.origin}, Куда: ${route.destination}
                <button onclick="editRoute(${route.id})">✏️</button>
                <button onclick="deleteRoute(${route.id})">🗑️</button>`;
            routeList.appendChild(li);
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

        document.getElementById('route-name').value = route.name;
        document.getElementById('route-origin').value = route.origin;
        document.getElementById('route-destination').value = route.destination;

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
        name: document.getElementById('route-name').value,
        origin: document.getElementById('route-origin').value,
        destination: document.getElementById('route-destination').value
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