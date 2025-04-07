document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const loginData = { email, password };

    try {
        const response = await fetch('https://ts.jijathecat.space/logistics/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.token); // Сохраняем токен в localStorage
            alert('Вы успешно вошли!');
            window.location.href = 'index.html'; // Перенаправляем на главную страницу
        } else {
            alert('Ошибка входа, проверьте свои данные');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});