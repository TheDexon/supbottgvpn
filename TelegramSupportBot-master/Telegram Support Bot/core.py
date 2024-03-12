import config
import datetime
import random
import psycopg2


# Добавить агента
def add_agent(agent_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("INSERT INTO agents (agent_id) VALUES (%s)", (agent_id,))
        con.commit()

        print("Agent added successfully.")

    except psycopg2.Error as e:
        print("Error adding agent:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Добавить файл
def add_file(req_id, file_id, file_name, type):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("INSERT INTO files (req_id, file_id, file_name, type) VALUES (%s, %s, %s, %s)",
                    (req_id, file_id, file_name, type))
        con.commit()

        print("File added successfully.")

    except psycopg2.Error as e:
        print("Error adding file:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Создать запрос
def new_req(user_id, request):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        # Добавить запрос в БД
        cur.execute("INSERT INTO requests (user_id, req_status) VALUES (%s, 'waiting') RETURNING req_id", (user_id,))
        req_id = cur.fetchone()[0]

        dt = datetime.datetime.now()
        date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

        # Добавить сообщение для запроса
        cur.execute("INSERT INTO messages (req_id, message, user_status, date) VALUES (%s, %s, 'user', %s)",
                    (req_id, request, date_now))

        con.commit()
        print("Request created successfully.")

        return req_id

    except psycopg2.Error as e:
        print("Error creating request:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Добавить сообщение
def add_message(req_id, message, user_status):
    try:
        if user_status == 'user':
            req_status = 'waiting'
        elif user_status == 'agent':
            req_status = 'answered'

        dt = datetime.datetime.now()
        date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        # Добавить сообщение для запроса
        cur.execute("INSERT INTO messages (req_id, message, user_status, date) VALUES (%s, %s, %s, %s)",
                    (req_id, message, user_status, date_now))

        # Изменить статус запроса
        cur.execute("UPDATE requests SET req_status = %s WHERE req_id = %s", (req_status, req_id))

        con.commit()
        print("Message added successfully.")

    except psycopg2.Error as e:
        print("Error adding message:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Добавить пароли
def add_passwords(passwords):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        for password in passwords:
            cur.execute("INSERT INTO passwords (password) VALUES (%s)", (password,))

        con.commit()

        print("Passwords added successfully.")

    except psycopg2.Error as e:
        print("Error adding passwords:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Проверить статус агента
def check_agent_status(user_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        # Преобразуйте user_id в строку, чтобы сравнение производилось правильно
        user_id_str = str(user_id)

        cur.execute("SELECT * FROM agents WHERE agent_id = %s", (user_id_str,))
        agent = cur.fetchone()

        print("Agent status checked successfully.")

        return agent is not None

    except psycopg2.Error as e:
        print("Error checking agent status:", e)

    finally:
        if con:
            cur.close()
            con.close()



# Проверить валидность пароля
def valid_password(password):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT * FROM passwords WHERE password = %s", (password,))
        password = cur.fetchone()

        print("Password validity checked successfully.")

        return password is not None

    except psycopg2.Error as e:
        print("Error checking password validity:", e)

    finally:
        if con:
            cur.close()
            con.close()


###########################

# Проверить отправляет ли пользователь файл, если да - вернуть его
def get_file(message):
    """
    Атрибут file_name доступен только в типах файлов - document и video.
    Если пользователь отправляет не документ и не видео - в качестве имени файла передать дату и время отправки (date_now)
    """

    types = ['document', 'video', 'audio', 'voice']
    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    # Сначала проверить отправляет ли пользователь фото
    try:
        return {'file_id': message.json['photo'][-1]['file_id'], 'file_name': date_now, 'type': 'photo',
                'text': str(message.caption)}

    # Если нет - проверить отправляет ли документ, видео, аудио, голосовое сообщение
    except:
        for type in types:
            try:
                if type == 'document' or type == 'video':
                    file_name = message.json[type]['file_name']
                else:
                    file_name = date_now

                return {'file_id': message.json[type]['file_id'], 'file_name': file_name, 'type': type,
                        'text': str(message.caption)}
            except:
                pass

        return None


# Получить иконку статуса запроса
def get_icon_from_status(req_status, user_status):
    if req_status == 'confirm':
        return '✅'

    elif req_status == 'waiting':
        if user_status == 'user':
            return '⏳'
        elif user_status == 'agent':
            return '❗️'

    elif req_status == 'answered':
        if user_status == 'user':
            return '❗️'
        elif user_status == 'agent':
            return '⏳'


# Получить текст для кнопки с файлом
def get_file_text(file_name, type):
    if type == 'photo':
        return f'📷 | Фото {file_name}'
    elif type == 'document':
        return f'📄 | Документ {file_name}'
    elif type == 'video':
        return f'🎥 | Видео {file_name}'
    elif type == 'audio':
        return f'🎵 | Аудио {file_name}'
    elif type == 'voice':
        return f'🎧 | Голосовое сообщение {file_name}'


# Сгенерировать пароли
def generate_passwords(number, length):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    passwords = []
    for _ in range(number):
        password = ''
        for _ in range(length):
            password += random.choice(chars)

        passwords.append(password)

    return passwords


# Получить юзер айди пользователя, создавшего запрос
def get_user_id_of_req(req_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT user_id FROM requests WHERE req_id = %s", (req_id,))
        user_id = cur.fetchone()[0]

        return user_id

    except psycopg2.Error as e:
        print("Error getting user id of request:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить file_id из id записи в БД
def get_file_id(id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT file_id FROM files WHERE id = %s", (id,))
        file_id = cur.fetchone()[0]

        return file_id

    except psycopg2.Error as e:
        print("Error getting file id:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить статус запроса
def get_req_status(req_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT req_status FROM requests WHERE req_id = %s", (req_id,))
        req_status = cur.fetchone()[0]

        return req_status

    except psycopg2.Error as e:
        print("Error getting request status:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Удалить пароль
def delete_password(password):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("DELETE FROM passwords WHERE password = %s", (password,))
        con.commit()

    except psycopg2.Error as e:
        print("Error deleting password:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Удалить агента
def delete_agent(agent_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("DELETE FROM agents WHERE agent_id = %s", (agent_id,))
        con.commit()

    except psycopg2.Error as e:
        print("Error deleting agent:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Завершить запрос
def confirm_req(req_id):
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("UPDATE requests SET req_status = 'confirm' WHERE req_id = %s", (req_id,))
        con.commit()

    except psycopg2.Error as e:
        print("Error confirming request:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить пароли с лимитом
def get_passwords(number):
    try:
        limit = (int(number) * 10) - 10

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT password FROM passwords LIMIT 10 OFFSET %s", (limit,))
        passwords = cur.fetchall()

        return passwords

    except psycopg2.Error as e:
        print("Error getting passwords:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить агентов с лимитом
def get_agents(number):
    try:
        limit = (int(number) * 10) - 10

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT agent_id FROM agents LIMIT 10 OFFSET %s", (limit,))
        agents = cur.fetchall()

        return agents

    except psycopg2.Error as e:
        print("Error getting agents:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить мои запросы с лимитом
def my_reqs(number, user_id):
    try:
        limit = (int(number) * 10) - 10

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT req_id, req_status FROM requests WHERE user_id = %s ORDER BY req_id DESC LIMIT 10 OFFSET %s", (str(user_id), limit))
        reqs = cur.fetchall()

        return reqs

    except psycopg2.Error as e:
        print("Error getting my requests:", e)

    finally:
        if con:
            cur.close()
            con.close()



# Получить запросы по статусу с лимитом
def get_reqs(number, callback):
    try:
        limit = (int(number) * 10) - 10
        req_status = callback.replace('_reqs', '')

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT req_id, req_status FROM requests WHERE req_status = %s ORDER BY req_id DESC LIMIT 10 OFFSET %s", (req_status, limit))
        reqs = cur.fetchall()

        return reqs

    except psycopg2.Error as e:
        print("Error getting requests by status:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить файлы по запросу с лимитом
def get_files(number, req_id):
    try:
        limit = (int(number) * 10) - 10

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT id, file_name, type FROM files WHERE req_id = %s ORDER BY id DESC LIMIT 10 OFFSET %s", (req_id, limit))
        files = cur.fetchall()

        return files

    except psycopg2.Error as e:
        print("Error getting files by request:", e)

    finally:
        if con:
            cur.close()
            con.close()


# Получить историю запроса
def get_request_data(req_id, callback):
    try:
        if 'my_reqs' in callback:
            get_dialog_user_status = 'user'
        else:
            get_dialog_user_status = 'agent'

        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("SELECT message, user_status, date FROM messages WHERE req_id = %s", (req_id,))
        messages = cur.fetchall()

        data = []
        text = ''
        i = 1

        for message in messages:
            message_value = message[0]
            user_status = message[1]
            date = message[2]

            if user_status == 'user':
                if get_dialog_user_status == 'user':
                    text_status = '👤 Ваше сообщение'
                else:
                    text_status = '👤 Сообщение пользователя'
            elif user_status == 'agent':
                text_status = '🧑‍💻 Агент поддержки'

            # Бэкап для текста
            backup_text = text
            text += f'{text_status}\n{date}\n{message_value}\n\n'

            # Если размер текста превышает допустимый в Telegram, то добавить первую часть текста и начать вторую
            if len(text) >= 4096:
                data.append(backup_text)
                text = f'{text_status}\n{date}\n{message_value}\n\n'

            # Если сейчас последняя итерация, то проверить не является ли часть текста превыщающий допустимый размер (4096 символов).
            # Если превышает - добавить часть и начать следующую. Если нет - просто добавить последнюю часть списка.
            if len(messages) == i:
                if len(text) >= 4096:
                    data.append(backup_text)
                    text = f'{text_status}\n{date}\n{message_value}\n\n'

                data.append(text)

            i += 1

        return data

    except psycopg2.Error as e:
        print("Error getting request data:", e)

    finally:
        if con:
            cur.close()
            con.close()