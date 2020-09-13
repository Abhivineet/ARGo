import mysql.connector

mydb=mysql.connector.connect(host='127.0.0.1', user='root', password='ninjahattori', database='TRACKING', auth_plugin='mysql_native_password')
mycursor = mydb.cursor()

sql = "SELECT * from user where name=" + '10218895930659400'

mycursor.execute(sql)

ret = mycursor.fetchall()

print(ret[0][1])