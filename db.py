import mysql.connector


class DataBase:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "recomendacaodb"

    def __connect__(self):
        self.con = mysql.connector.connect(
          host=self.host,
          user=self.user,
          password=self.password,
          database=self.db
        )
        self.cursor = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def execute(self, sql):
        self.__connect__()
        self.cursor.execute(sql)
        self.con.commit()
        self.__disconnect__()
