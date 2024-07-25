import psycopg2

class ConnexionPostgress:
    """Constructor que inicia conexion a base de datos"""
    def __init__(self):
        try:
            self._conexion = psycopg2.connect(
                host = 'localhost',
                port = '5432',
                user = 'postgres',
                password = 'admin',
                database = 'mydatabase'
                
            )
            print("Conexion correcta")                  

        except Exception as exception:
            print(exception)
    
    """Crear tabla"""
    def createTable(self, logger):
        self._cursor = self._conexion.cursor()        
        sql_create = """CREATE TABLE IF NOT EXISTS robot(
            name_robot TEXT PRIMARY KEY,
            status_creation TEXT,
            status_pdf TEXT,
            path_pdf TEXT,
            status_final TEXT
        )"""
        self._cursor.execute(sql_create)
        self._conexion.commit()
        logger.setMessage("Tabla creada",'info')
        print("Tabla creada ")

    """Hacer insert en la tabla pidiendo los datos al usuario"""
    def insert (self,logger):
        self._cursor = self._conexion.cursor()
        sql = 'INSERT INTO robot(name_robot,status_creation,status_pdf,path_pdf,status_final) values (%s,%s,%s,%s,%s)'
        nombre = input("Ingrese nombre robot: ")
        status = input("Ingrese estado de creacion: ")
        status_pdf = input("Ingrese estado pdf: ")
        path = input('Ingrese path pdf: ')
        final_status = input("Ingrese estado final: ")

        datos = (nombre,status,status_pdf,path,final_status)
        self._cursor.execute(sql,datos)
        #guardar datos
        self._conexion.commit()
        logger.setMessage("Datos insertados a la base de datos",'info')
        print("Datos insertados ")

    """Cerrar conexion"""
    def closeConexion(self,logger):
        self._cursor = self._conexion.cursor()
        self._cursor.close()
        self._conexion.close()
        logger.setMessage("Conexion a la base de datos cerrada",'info')
        print("Base de datos cerrada ")

