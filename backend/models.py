import mysql.connector


class ServiceOffre(object):

    def __init__(self, id_offre, status):
        self.id_offre = id_offre
        self.status = status

    def init_connexion(self):
        cnx = mysql.connector.connect(user=self.mysql_user, password=self.mysql_password,
                                      host=self.mysql_host, database=self.mysql_database)
