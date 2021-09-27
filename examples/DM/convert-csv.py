import sqlite3 as sql
import os
import csv
from sqlite3 import Error

try:

    # Connect to database
    conn = sql.connect('/media/sf_snippets/snippets.db')
    cursor = conn.cursor()
    cursor.execute('''select * from snippets where language='Python' LIMIT 100''')
    #rows =  cursor.fetchall()
    #print(rows)
    with open("python_data.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/python_data.csv"
    print("Data exported Successfully into {}".format(dirpath))

except Error as e:
    print(e)

# Close database connection
finally:
    conn.close()