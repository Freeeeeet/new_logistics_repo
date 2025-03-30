const apiUrl = 'https://ts.jijathecat.space/logistics/api';

// Переключение вкладок
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(tabId).style.display = 'block';
}

// Создание клиента
document.getElementById('client-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const clientId = document.getElementById('client-id').value;  // Проверяем, редактируем или создаем
    const clientName = document.getElementById('client-name').value;
    const clientEmail = document.getElementById('client-email').value;
    const clientPhone = document.getElementById('client-phone').value;

    const clientData = {
        name: clientName,
        email: clientEmail,
        phone: clientPhone
    };

    try {
        let response;
        if (clientId) {
            // Если есть clientId, то редактируем клиента
            response = await fetch(`${apiUrl}/clients/${clientId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clientData)
            });
        } else {
            // Иначе создаем нового клиента
            response = await fetch(`${apiUrl}/clients/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clientData)
            });
        }

        if (response.ok) {
            alert(clientId ? 'Клиент обновлен!' : 'Клиент создан!');
            document.getElementById('client-form').reset();
            document.getElementById('client-id').value = '';  // Очистка скрытого поля
            getClients();
        } else {
            alert('Ошибка при сохранении клиента');
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
                <button onclick="editClient(${client.id}, '${client.name}', '${client.email}', '${client.phone}')">✏ Редактировать</button>
                <button onclick="deleteClient(${client.id})">🗑 Удалить</button>
            `;
            clientList.appendChild(li);
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Функция для редактирования клиента
function editClient(id, name, email, phone) {
    document.getElementById('client-id').value = id;
    document.getElementById('client-name').value = name;
    document.getElementById('client-email').value = email;
    document.getElementById('client-phone').value = phone;
}

// Функция для удаления клиента
async function deleteClient(clientId) {
    if (!confirm('Вы уверены, что хотите удалить этого клиента?')) return;

    try {
        const response = await fetch(`${apiUrl}/clients/${clientId}`, { method: 'DELETE' });

        if (response.ok) {
            alert('Клиент удален!');
            getClients();
        } else {
            alert('Ошибка при удалении клиента');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Загрузка клиентов при открытии страницы
getClients();
showTab('clients');