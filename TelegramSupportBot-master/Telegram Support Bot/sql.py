import config
import psycopg2


def create_table_agents():
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS agents(id SERIAL PRIMARY KEY, agent_id VARCHAR(20))")

        con.commit()
        print("Table 'agents' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table 'agents':", e)

    finally:
        if con:
            cur.close()
            con.close()


def create_table_passwords():
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS passwords(id SERIAL PRIMARY KEY, password VARCHAR(20))")

        con.commit()
        print("Table 'passwords' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table 'passwords':", e)

    finally:
        if con:
            cur.close()
            con.close()


def create_table_files():
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS files(id SERIAL PRIMARY KEY, req_id VARCHAR(20), file_id VARCHAR(250), file_name VARCHAR(2048), type VARCHAR(20))")

        con.commit()
        print("Table 'files' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table 'files':", e)

    finally:
        if con:
            cur.close()
            con.close()


def create_table_requests():
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS requests(req_id SERIAL PRIMARY KEY, user_id VARCHAR(20), req_status VARCHAR(20))")

        con.commit()
        print("Table 'requests' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table 'requests':", e)

    finally:
        if con:
            cur.close()
            con.close()


def create_table_messages():
    try:
        con = psycopg2.connect(
            host=config.PostgreSQL[0],
            user=config.PostgreSQL[1],
            password=config.PostgreSQL[2],
            database=config.PostgreSQL[3]
        )
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS messages(id SERIAL PRIMARY KEY, req_id VARCHAR(20), message VARCHAR(4096), user_status VARCHAR(20), date VARCHAR(50))")

        con.commit()
        print("Table 'messages' created successfully.")

    except psycopg2.Error as e:
        print("Error creating table 'messages':", e)

    finally:
        if con:
            cur.close()
            con.close()


create_table_agents()
create_table_passwords()
create_table_files()
create_table_requests()
create_table_messages()
