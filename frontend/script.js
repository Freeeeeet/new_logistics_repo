document.getElementById('orderForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Не даем форме отправиться

    const clientId = document.getElementById('client').value;
    const cargoDescription = document.getElementById('cargo').value;
    const routeId = document.getElementById('route').value;

    // Структура данных для нового заказа
    const orderData = {
        client_id: clientId,
        cargo_description: cargoDescription,
        route_id: routeId,
        status_id: 1  // Статус заказа (по умолчанию 1)
    };

    try {
        // Отправка данных на бэкенд
        const response = await fetch('http://backend:8000/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });

        if (!response.ok) {
            throw new Error('Ошибка при создании заказа');
        }

        const result = await response.json();
        alert(`Заказ создан! ID: ${result.id}`);
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
    }
});