import psycopg2

#print(f'''INSERT INTO Client(id, name, surname, email)
#VALUES({id}, {name}, {surname});
      #        ''')
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
              CREATE TABLE IF NOT EXISTS Client(
                  id SERIAL PRIMARY KEY,
                  name VARCHAR(40) NOT NULL,
                  surname VARCHAR(40) NOT NULL,
                  email VARCHAR(40) NOT NULL
              );
              """)
        cur.execute("""
              CREATE TABLE IF NOT EXISTS Phone_number(
                  client_id int REFERENCES Client(id),
                  number INTEGER NOT NULL UNIQUE
              );
              """)
        conn.commit()  # фиксируем в БД
    pass

def add_client(conn, name, surname, email, phone=None):
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
        cur.execute(f"INSERT INTO Phone_number(client_id, number) VALUES({client_id}, {phone});")
        conn.commit()  # фиксируем в БД

def change_client(conn, client_id, value):
    with conn.cursor() as cur:
        cur.execute(f"""UPDATE Client SET {value} WHERE id = {client_id};
        """)
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

with psycopg2.connect(database='test1', user='postgres', password='Dreddred0102-') as conn:
    create_db(conn)
    surname = input('Введите Фамилию ')
    name = input('Введите Имя ')
    email = input('Введите электронную почту ')
    #number = input('Если у клиента есть номер  телефона, введите y ')
    phone = None
    add_client(conn, name, surname, email, phone=None)

