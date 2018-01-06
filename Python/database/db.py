import mysql.connector
from mysql.connector import errorcode


class Db(object):
	def __init__(self):
		try:
			self.cnx = mysql.connector.connect(
							user='root', password='23238022', host='127.0.0.1', database='MFCom')
			self.cursor = self.cnx.cursor()
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)


	def query(self,q):
		self.cursor.execute(q)
		results = self.cursor.fetchall()
		attributes = self.cursor.column_names
		return attributes, results

	def close(self):
		self.cnx.commit()
		self.cursor.close()
		self.cnx.close()

if __name__ == '__main__':
	p = Db()
	a,r = p.query('SELECT * FROM Member;')
	print(a)
	print(r)
