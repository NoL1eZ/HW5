import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
              CREATE TABLE IF NOT EXISTS Client(
                  id SERIAL PRIMARY KEY,
                  name VARCHAR(40) NOT NULL,
                  surname VARCHAR(40) NOT NULL,
                  email VARCHAR(40) NOT NULL UNIQUE
              );
              """)
        conn.commit()
        cur.execute("""
              CREATE TABLE IF NOT EXISTS Phone_number(
                  client_id int REFERENCES Client(id),
                  number INTEGER NOT NULL UNIQUE
              );
              """)
        conn.commit()  # фиксируем в БД
    pass

def add_client(conn,name, surname, email, phone):
    with conn.cursor() as cur:
        postgres_insert_query = "INSERT INTO Client(name, surname, email) VALUES(%s,%s,%s)RETURNING id;"
        record_to_insert = (name, surname, email)
        cur.execute(postgres_insert_query, record_to_insert)
        value = cur.fetchone()  # фиксируем в БД
        if phone != None:
            cur.execute(f"""INSERT INTO Phone_number(client_id, number) VALUES({value[0]}, {phone});
            """)
        conn.commit()  # фиксируем в БД
    pass

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f"""INSERT INTO Phone_number(client_id, number) VALUES({client_id}, {phone});
        """)
        conn.commit()  # фиксируем в БД

def change_client(conn, client_id, info, value):
    with conn.cursor() as cur:
        postgres_insert_query = f"UPDATE Client SET {info} = %s WHERE id = %s;;"
        record_to_insert = (value, client_id)
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()  # фиксируем в БД
    pass

def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute(f"""DELETE FROM Phone_number WHERE number = {phone};
        """)
        conn.commit()  # фиксируем в БД
    pass

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f"""DELETE FROM Phone_number WHERE client_id = {client_id};
        """)
        cur.execute(f"""DELETE FROM Client WHERE id = {client_id};
        """)
        conn.commit()
    pass

def find_client(conn, value_name, value):
    with conn.cursor() as cur:
        postgres_insert_query = None
        record_to_insert = (value,)
        if value_name == 'e':
            postgres_insert_query = """SELECT name, surname, email, number FROM Client
                    FUll JOIN Phone_number ON Client.id = Phone_number.client_id
                    WHERE email = %s; 
                    """

        elif value_name == 'n':
            record_to_insert = (int(value),)
            postgres_insert_query = """SELECT name, surname, email, number FROM Client
                            FUll JOIN Phone_number ON Client.id = Phone_number.client_id
                            WHERE number = %s; 
                            """
        cur.execute(postgres_insert_query, record_to_insert)
        print(cur.fetchall())
    pass

if __name__ == '__main__':
    with psycopg2.connect(database='HW5', user='postgres', password='Dreddred0102-') as conn:
        while True:
            command = input('Что вы хотите сделать ')
            if command.lower() == 'ccc':
                create_db(conn)

            elif command.lower() == 'ac':
                surname = input('Введите Фамилию ')
                name = input('Введите Имя ')
                email = input('Введите электронную почту ')
                number = input('Если у клиента есть номер  телефона, введите y ')
                phone = None
                if number == 'y':
                    phone = int(input('Введите номер телефона '))
                add_client(conn, name, surname, email, phone)

            elif command.lower() == 'ap':
                client_id = int(input('Введите номер клиента '))
                phone = int(input('Введите номер телефона '))
                add_phone(conn, client_id, phone)

            elif command.lower() == 'cc':
                client_id = int(input('Введите номер клиента '))
                info = input('Введите название столбца в котором хотите изменить информацию ')
                value = input('Введите значение ')
                change_client(conn, client_id, info, value)

            elif command.lower() == 'dp':
                phone = int(input('Введите номер телефона '))
                delete_phone(conn, phone)

            elif command.lower() == 'dc':
                client_id = int(input('Введите номер клиента '))
                delete_client(conn, client_id)

            elif command.lower() == 'sc':
                value_name = input('Поиск производится по электронной почте "e" и номеру телефона "n": ')
                value = input('Введите значение ')
                find_client(conn, value_name, value)