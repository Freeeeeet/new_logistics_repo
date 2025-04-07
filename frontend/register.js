document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const full_name = document.getElementById('register-fullname').value;

    const registerData = { username, email, full_name, password };

    try {
        const response = await fetch('https://ts.jijathecat.space/logistics/api/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(registerData)
        });

        if (response.ok) {
            alert('Вы успешно зарегистрированы! Можете войти.');
            window.location.href = 'login.html'; // Перенаправляем на страницу входа
        } else {
            alert('Ошибка регистрации');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});