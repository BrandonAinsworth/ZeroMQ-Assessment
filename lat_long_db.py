import psycopg2



def connect_to_db():
  connection = None
  try:
    connection = psycopg2.connect(
        database='0MQ', 
        user='brandonainsworth'
        )
    print('Database connection successful')
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  return connection

def write_radians_to_db(message):
  
  connection = connect_to_db()
  cur = connection.cursor()
  
  try:
    cur.execute(f'''
                INSERT INTO "public.lat_long_messages"(lat_rad, long_rad) 
                VALUES({message['lat_rad']},{message['long_rad']});
                ''')
    connection.commit()
    print('Query Successful')
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
      print(error)
  

      