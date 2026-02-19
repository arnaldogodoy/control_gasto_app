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
        consulta = "select id from usuario where email = %s and password = %s and activo = 1"
        cursor.execute(consulta, params=(correo,clave))
        resultado = cursor.fetchone()
        if resultado:
            return True, resultado
        else:
            return False, None
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

def obtiene_tipos_tarjetas():
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """select id, tipo from tarjeta_credito_tipo where activo = 1"""
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        if resultados:
            return resultados
        else:
            print("No hay tipos de tarjetas habilitados")
    except Exception as er:
        print(f"Error al obtener los tipos de tarjetas: {er}")
    finally:
        cursor.close()

def obtiene_bancos():
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """select id, banco from banco where activo = 1 order by banco"""
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        if resultados:
            return resultados
        else:
            print("No hay bancos habilitados")
    except Exception as er:
        print(f"Error al obtener los bancos disponibles: {er}")
    finally:
        cursor.close()

def crea_tarjeta_credito(id_usuario, ultimos_numeros, id_tipo, fecha_vencimiento_tarjeta, limite_credito, dia_cierre_resumen, dia_vencimiento_resumen, id_banco, alias):
    try:
        cursor = conexion.cursor()
        consulta_insert = """insert into tarjeta_credito (id_usuario,ultimos_numeros,id_tipo,fecha_vencimiento,limite,dia_cierre_resumen,dia_vence_resumen,id_banco,activa,alias)
        values (%s,%s,%s,%s,%s,%s,%s,%s,1,%s)
        """
        cursor.execute(consulta_insert,(id_usuario,ultimos_numeros,id_tipo,fecha_vencimiento_tarjeta,limite_credito,dia_cierre_resumen,dia_vencimiento_resumen,id_banco,alias))
        conexion.commit()
        return True
    except Exception as er:
        print(f"Error al insertar la nueva tarjeta de credito: {er}")
        conexion.rollback()
        return None
    finally:
        cursor.close()

def obtiene_tarjetas_por_usuario(id_usuario : int):
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
                    select
                        tc.id id_tarjeta,
                        ultimos_numeros,
                        fecha_vencimiento,
                        limite,
                        dia_cierre_resumen,
                        dia_vence_resumen,
                        tipo,
                        banco,
                        alias
                    from tarjeta_credito tc
                    left join tarjeta_credito_tipo tct on tct.id = tc.id_tipo
                    left join banco b on b.id = tc.id_banco
                    where id_usuario = %s and activa = 1"""
        cursor.execute(consulta,(id_usuario,))
        resultados = cursor.fetchall()
        if resultados:
            return resultados
        else:
            print("El cliente no tiene tarjetas asociadas")
    except Exception as er:
        print("Ocurrio un error al obtener las tarjetas de credito")
        raise
    finally:
        cursor.close()

def deshabilita_usuario_tarjeta_id(id_usuario : int,id_tarjeta : int,):
    try:
        cursor = conexion.cursor()
        consulta_update = "update tarjeta_credito set activa = 0 where id_usuario = %s and id = %s"
        cursor.execute(consulta_update, (id_usuario,id_tarjeta))
        conexion.commit()
        return True
    except Exception as er:
        conexion.rollback()
        print(f"Error al actualizar: {er}")
        return False  
    finally:
        cursor.close()

def editar_usuario_tarjeta_id(alias : str, limite,dia_cierre_resumen : int, dia_vence_resumen : int, id_usuario : int ,id_tarjeta : int):
    try:
        cursor = conexion.cursor()
        consulta_update = "update tarjeta_credito set alias = %s ,limite = %s ,dia_cierre_resumen = %s ,dia_vence_resumen = %s where id_usuario = %s and id = %s"
        cursor.execute(consulta_update, (alias,limite, dia_cierre_resumen,dia_vence_resumen,id_usuario,id_tarjeta))
        conexion.commit()
        return True
    except Exception as er:
        conexion.rollback()
        print(f"Error al actualizar: {er}")
        return False  
    finally:
        cursor.close()

def obtener_categorias_por_usuario(id_usuario : int):
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
        select 
            gc.id id_categoria,
            gc.categoria,
            gc.id_usuario,
            gca.nombre agrupador,
            gca.icono
        from gasto_categoria gc
        left join gasto_categoria_agrupador gca on gc.id_categoria_agrupador = gca.id
        where 
            gc.activa = 1 
            and (gc.id_usuario is null or gc.id_usuario = %s)
        order by gca.id;
        """
        cursor.execute(consulta, (id_usuario,))
        resultados = cursor.fetchall()
        return resultados if resultados else []
    except Exception as e:
        print(f"Error al obtener las categorias: {e}")
        return[]
    finally:
        if cursor:
            cursor.close()


