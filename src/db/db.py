import mysql.connector
#import logging
from config import config

#logging.basicConfig(level=logging.DEBUG) 

#Conexion a la base de datos:
conexion = mysql.connector.connect(
    host=config.host,
    port=config.port,
    user=config.user,
    password=config.password,
    database=config.database,
)


def logea_usuario(correo, clave):
    try:
        cursor = conexion.cursor()
        consulta = "select 1 from usuario where email = %s and password = %s and activo = 1"
        cursor.execute(consulta, params=(correo,clave))
        resultado = cursor.fetchone()
        if resultado:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al logear usuario: {e}")
        return False
    finally:
        cursor.close()

def validar_preguntas(correo , respuesta1, respuesta2):
    try:
        correo = correo.lower()
        respuesta1 = respuesta1.lower()
        respuesta2 = respuesta2.lower()
        cursor = conexion.cursor()
        consulta = """select respuesta from usuario u
                    left join usuario_pregunta_clave upc on upc.id_usuario = u.id
                    where email = %s and respuesta in (%s,%s)"""
        cursor.execute(consulta, params=(correo,respuesta1,respuesta2))
        resultado = cursor.fetchall()
        if len(resultado) == 2:
            return True
        else:
            return False
    except Exception as er:
        print(f"Error al validar las respuestas: {er}")
    finally:
        cursor.close()

def obtiene_preguntas_por_usuario(correo):
    try:
        print(correo)
        cursor = conexion.cursor()
        consulta = """select pregunta from usuario u 
                    left join usuario_pregunta_clave upc on u.id = upc.id_usuario
                    left join pregunta_clave pc on pc.id = upc.id_pregunta
                    where upc.activo = 1 and u.email = %s"""
        cursor.execute(consulta,(correo,))
        resultado = cursor.fetchall()
        print(resultado)
        return [row[0] for row in resultado] if resultado else []
    except Exception as er:
        print(f"Error al obtener las preguntas: {er} ")
        return []
    finally:
        cursor.close()

def actualiza_contraseña_por_usuario(contraseña, email):
    try:
        cursor = conexion.cursor()
        consulta_insert = "update usuario set password = %s where email = %s"
        cursor.execute(consulta_insert, (contraseña,email))
        conexion.commit()
        return True
    except Exception as er:
        conexion.rollback()
        print(f"Error al actualizar: {er}")
        return False  
    finally:
        cursor.close()

def obtiene_contraseña_por_usuario(email):
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """select password from usuario where email = %s limit 1"""
        cursor.execute(consulta,(email,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as er:
        print(f"Error al obtener contraseña: {er}")
    finally:
        cursor.close()

def obtiene_preguntas_seguridad_registro():
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """select id, pregunta from pregunta_clave where activo = 1"""
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        return resultado
    except Exception as er:
        print("Ocurrio un error al obtener las preguntas de seguridad")
        return False
    finally:
        cursor.close()

def valida_email_registro(email):
    try:
        cursor = conexion.cursor()
        email = email.lower()
        consulta = """select sum(1) from usuario where email = %s"""
        cursor.execute(consulta, (email,))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    except Exception as er:
        print(f"Ocurrio un error al validar el correo electronico en el registro: {er}")
        return None
    finally:
        cursor.close()
        
def crea_usuario(nombre, apellido , email, contraseña, id_pregunta1, respuesta1, id_pregunta2, respuesta2 ):
    try:
        cursor = conexion.cursor()
        nombre = nombre.lower()
        apellido = apellido.lower()
        email = email.lower()
        respuesta1 = respuesta1.lower()
        respuesta2 = respuesta2.lower()
        insert_usuario = """
        insert into usuario (nombre,apellido,email,password,activo) values (%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_usuario,(nombre,apellido,email,contraseña,1))
        ultimo_id = cursor.lastrowid
        insert_pregunta = """
        insert into usuario_pregunta_clave (id_usuario,id_pregunta,respuesta,activo) values(%s,%s,%s,1)
        """
        cursor.execute(insert_pregunta,(ultimo_id,id_pregunta1,respuesta1))
        cursor.execute(insert_pregunta,(ultimo_id,id_pregunta2,respuesta2))
        conexion.commit()
        return True
    except Exception as er:
        print("Ocurrio un error al momento de crear el usuario")
    finally:
        cursor.close()


