import MySQLdb

class Database:
  host = 'localhost'
  user = 'root'
  password = 'asd'
  db = 'sensors'
  
  def __init__(self):
    sensors = ['dht11_temperature','dht11_humidity','sound','light','temperature']
    self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
    self.cursor = self.connection.cursor()
  	
  	for sensor in sensors:
      try:
      	q ='''CREATE TABLE {0} (
        	    id INT NOT NULL AUTO_INCREMENT,
        	    value INT, 
         	    unit VARCHAR(100), 
        	    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        	    PRIMARY KEY ( id ) )
              '''.format(sensor)
      	self.cursor.execute(q)
      	self.connection.commit()
      except:
      	self.connection.rollback()

  def insert(self, query):
  	try:
      self.cursor.execute(query)
      self.connection.commit()
    except:
      self.connection.rollback()

  def query(self, query):
    cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
    cursor.execute(query)

    return cursor.fetchall()

  def __del__(self):
    self.connection.close()