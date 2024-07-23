from src.ConnexionPostgress import ConnexionPostgress

def main():
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()

    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("Ingrese 1 para Crear tabla, 2 para hacer INSERT"))    
    # match case
    match num:
        case num if num == 1:
            database.createTable()
        case num if num == 2:
            database.insert() 
        case _:
            print("Error") 
    """Cerrar base de datos"""
    database.closeConexion()


if(__name__ == '__main__'):
    main()