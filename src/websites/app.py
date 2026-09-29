from flask import Flask, render_template, request, jsonify
import mysql.connector
import bcrypt  # Установите: pip install bcrypt

app = Flask(__name__)

# Отключаем ASCII-экранирование в JSON, чтобы кириллица выводилась нормально
# Для Flask 2.3+:
app.json.ensure_ascii = False
# Для Flask < 2.3 (если верхняя строка вызовет ошибку, используйте эту):
# app.config['JSON_AS_ASCII'] = False


@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()

    # Подключение к БД
    cnx = mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123"
    )

    name = req['name']
    login = req['email']
    password = req['password']

    # Хеширование пароля
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Сохраняем хеш в БД (как строку)
    date = (name, login, hashed_password.decode('utf-8'))

    cur = cnx.cursor()
    try:
        cur.execute(
            'INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)',
            date
        )
        cnx.commit()
        response = {'status': 'success', 'message': 'Пользователь зарегистрирован!'}
    except mysql.connector.IntegrityError:
        # Если email уже существует
        response = {'status': 'error', 'message': 'Пользователь с таким email уже существует!'}
    finally:
        cur.close()
        cnx.close()

    return jsonify(response)


@app.route('/user_login', methods=['POST'])
def user_login():
    req = request.get_json()

    cnx = mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123"
    )

    login = req['name']
    password = req['password']

    cur = cnx.cursor()
    cur.execute('SELECT `password_hash` FROM `users` WHERE `email` = %s', (login,))
    result = cur.fetchone()
    print(result)
    #if result:
        #stored_hash = result[0]  # Получаем хеш из БД

        # Проверяем пароль
    response = {'status': 'success', 'message': 'Вход выполнен успешно!'}
    #else:
        #response = {'status': 'error', 'message': 'Пользователь не найден!'}

    cur.close()
    cnx.close()

    return jsonify(response)


@app.route("/")
def registration():
    return render_template('registration.html')


@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)