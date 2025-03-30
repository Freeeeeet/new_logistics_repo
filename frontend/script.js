const apiUrl = 'https://ts.jijathecat.space/logistics/api';  // Бэкенд на сервере

// Ждем загрузки DOM перед выполнением
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");
    getClients();
    showTab('clients');
});

// Переключение вкладок
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.getElementById(tabId).style.display = 'block';
}

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
            li.innerHTML = `
                Имя: ${client.name}, Email: ${client.email}, Телефон: ${client.phone}
                <button onclick="editClient(${client.id})">✏️</button>
                <button onclick="deleteClient(${client.id})">🗑️</button>
            `;
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