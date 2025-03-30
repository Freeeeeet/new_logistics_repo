const apiUrl = 'https://ts.jijathecat.space/logistics/api';

// Переключение вкладок
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(tabId).style.display = 'block';
}

// Создание или редактирование клиента
document.getElementById('client-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const clientId = document.getElementById('client-id').value.trim(); // Получаем ID клиента
    const clientName = document.getElementById('client-name').value.trim();
    const clientEmail = document.getElementById('client-email').value.trim();
    const clientPhone = document.getElementById('client-phone').value.trim();

    if (!clientName || !clientEmail || !clientPhone) {
        alert('Заполните все поля');
        return;
    }

    const clientData = { name: clientName, email: clientEmail, phone: clientPhone };

    try {
        let response;
        if (clientId) {
            console.log(`Редактируем клиента ID ${clientId}`, clientData);
            response = await fetch(`${apiUrl}/clients/${clientId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clientData)
            });
        } else {
            console.log('Создаём нового клиента', clientData);
            response = await fetch(`${apiUrl}/clients/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clientData)
            });
        }

        if (response.ok) {
            alert(clientId ? 'Клиент обновлён!' : 'Клиент создан!');
            document.getElementById('client-form').reset();
            document.getElementById('client-id').value = ''; // Сбрасываем ID после редактирования
            getClients();
        } else {
            const errorMessage = await response.text();
            alert(`Ошибка: ${errorMessage}`);
        }
    } catch (error) {
        console.error('Ошибка при отправке запроса:', error);
        alert('Ошибка сети. Проверьте консоль.');
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
                <span>Имя: ${client.name}, Email: ${client.email}, Телефон: ${client.phone}</span>
                <button onclick="editClient(${client.id}, '${client.name}', '${client.email}', '${client.phone}')">✏ Редактировать</button>
                <button onclick="deleteClient(${client.id})">🗑 Удалить</button>
            `;
            clientList.appendChild(li);
        });

        console.log('Клиенты загружены:', clients);
    } catch (error) {
        console.error('Ошибка загрузки клиентов:', error);
    }
}

// Заполняем форму для редактирования
function editClient(id, name, email, phone) {
    console.log(`Выбрали клиента ID ${id} для редактирования`);
    document.getElementById('client-id').value = id;
    document.getElementById('client-name').value = name;
    document.getElementById('client-email').value = email;
    document.getElementById('client-phone').value = phone;
}

// Удаление клиента
async function deleteClient(clientId) {
    if (!confirm('Удалить клиента?')) return;

    try {
        const response = await fetch(`${apiUrl}/clients/${clientId}`, { method: 'DELETE' });

        if (response.ok) {
            alert('Клиент удалён');
            getClients();
        } else {
            const errorMessage = await response.text();
            alert(`Ошибка удаления: ${errorMessage}`);
        }
    } catch (error) {
        console.error('Ошибка при удалении клиента:', error);
    }
}

// Загружаем клиентов при запуске
getClients();
showTab('clients');