from database.schema.table_tasks_schema import table_schema
from database.schema.user_schema import user_table_schema
import mysql.connector

try:
   db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="jaysingh@89",
      database="task_management_db"
    )
   if db.is_connected():
      cursor=db.cursor()
      print("Connected to database")
      cursor.execute(user_table_schema)
      cursor.execute(table_schema)

      db.commit()
      print("Tables created successfully")
except mysql.connector.Error as err:
   print(f"Error: {err}")

finally:
     if db.is_connected():
      cursor.close()
      db.close()
      print("Database connection closed")

      