from src.ConnexionPostgress import ConnexionPostgress

def main():
    database = ConnexionPostgress()
    database.createTable()
    #database.insert()    
    database.closeConexion()


if(__name__ == '__main__'):
    main()