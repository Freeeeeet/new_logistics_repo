// Изменяем URL для запросов на адрес бэкенда в Docker
const apiUrl = 'http://backend:8000';  // Используем имя контейнера

document.getElementById('client-form').addEventListener('submit', async (event) => {
  event.preventDefault();

  const clientName = document.getElementById('client-name').value;
  const clientEmail = document.getElementById('client-email').value;
  const clientPhone = document.getElementById('client-phone').value;

  const newClient = {
    name: clientName,
    email: clientEmail,
    phone: clientPhone
  };

  try {
    const response = await fetch(`${apiUrl}/clients/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newClient)
    });

    if (response.ok) {
      alert('Клиент создан!');
      getClients(); // обновляем список клиентов
    } else {
      alert('Ошибка при создании клиента');
    }
  } catch (error) {
    console.error('Ошибка:', error);
  }
});

// Функция для получения списка клиентов
async function getClients() {
  try {
    const response = await fetch(`${apiUrl}/clients/`);
    const clients = await response.json();
    const clientList = document.getElementById('clients-list');
    clientList.innerHTML = '';

    clients.forEach(client => {
      const li = document.createElement('li');
      li.textContent = `Имя: ${client.name}, Email: ${client.email}, Телефон: ${client.phone}`;
      clientList.appendChild(li);
    });
  } catch (error) {
    console.error('Ошибка:', error);
  }
}

// Загружаем клиентов при загрузке страницы
getClients();