#!/usr/bin/python3
import MySQLdb


class DBase(object):
    """Using DBase"""
    def __init__(self, access):
        self.conn = MySQLdb.connect("127.0.0.1", access["user"], access["password"], access["dbname"])

    def chekStatusUuid(self):
        cursor = self.conn.cursor()
        sql = "SELECT ETIQUETA_PUBLICITARIA_ID, UUID, COMPANION_GOOGLE, SITIO_APLICACION_ID, " \
              "MOSTRAR_DISPLAY_VIDEO_DESKTOP, PORCENTAJE_WEB, PORCENTAJE_MOBILE, STATUS_SCRIPT, " \
              "FORMATO, MODO, VIDEO_ESPECIFICACION, MOSTRAR_DISPLAY_VIDEO_MOBILE, PROGRAMACION_ANUNCIO," \
              "POSICION_ANUNCIO, MAPEO_ANUNCIO, MODO_SEGURO, INTERACTIVO "\
              "FROM etiqueta_publicitaria "\
              "WHERE STATUS_SCRIPT=1 OR STATUS_SCRIPT=5"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def updateStatusUuid(self, status, etiqueta):
        now = "NOW()"
        if status == 3:
            now = 'NULL'
        cursor = self.conn.cursor()
        sql = "UPDATE etiqueta_publicitaria "\
              "SET STATUS_SCRIPT=%d,FECHA_CREACION_SCRIPT=%s "\
              "WHERE ETIQUETA_PUBLICITARIA_ID=%d" % (status, now, etiqueta)
        cursor.execute(sql)
        self.conn.commit()
        results = cursor.rowcount
        cursor.close()
        return results

    def getAdTagScript(self, etiquetaID):
        cursor = self.conn.cursor()
        sql = "SELECT e.SCRIPT, e.ETIQUETA_NOMBRE_SSP, e.TIPO, e.APLICA_OFERTA, e.CPM, e.CPM_DECREMENTO, e.CPM_MIN "\
              "FROM etiqueta_video_ssp e "\
              "JOIN ssp s "\
              "ON e.SSP_ID = s.SSP_ID "\
              "WHERE e.ACTIVO=b'1' AND e.ETIQUETA_PUBLICITARIA_ID=%s AND e.SCRIPT IS NOT NULL AND e.SCRIPT<>''"\
              "ORDER BY s.PRIORIDAD ASC" % (etiquetaID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getDisplayTagScript(self, etiquetaID):
        cursor = self.conn.cursor()
        sql = "SELECT s.SSP_ID, s.IDENTIFICADOR,e.SCRIPT, e.TIPO, e.ANCHO, e.ALTO "\
              "FROM etiqueta_display_ssp e "\
              "JOIN ssp s "\
              "ON e.SSP_ID = s.SSP_ID "\
              "WHERE e.ACTIVO=b'1' AND e.ETIQUETA_PUBLICITARIA_ID=%s AND e.SCRIPT IS NOT NULL AND e.SCRIPT<>''"\
              "ORDER BY s.PRIORIDAD ASC" % (etiquetaID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getBlackList(self, SITIO_APLICACION_ID):
        cursor = self.conn.cursor()
        sql = "SELECT URL "\
              "FROM lista_negra "\
              "WHERE SITIO_APLICACION_ID=%d" % (SITIO_APLICACION_ID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getRelapUrl(self, SITIO_APLICACION_ID):
        cursor = self.conn.cursor()
        sql = "SELECT URL "\
              "FROM sitio_aplicacion "\
              "WHERE SITIO_APLICACION_ID=%d" % (SITIO_APLICACION_ID)
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

    def getConfigurationVideoIma(self):
        cursor = self.conn.cursor()
        sql = "SELECT ATRIBUTO1, VALOR "\
              "FROM bs_catalogo_general "\
              "WHERE DOMINIO LIKE '%CONFIGURACION_VIDEO_IMA%'"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getVideo(self, LISTA_REPRODUCCION_VIDEO_ID):
        cursor = self.conn.cursor()
        sql = "SELECT TITULO, URL_IMAGEN, DESCRIPCION, URL_DESCRIPCION, URL_VIDEO, " \
              "URL_LOGO, URL_DERECHOS_AUTOR, DERECHOS_AUTOR "\
              "FROM video "\
              "WHERE LISTA_REPRODUCCION_VIDEO_ID=%d" % (LISTA_REPRODUCCION_VIDEO_ID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getSiteConfigurationVideo(self, SITIO_APLICACION_ID):
        cursor = self.conn.cursor()
        sql = "SELECT APLICA_IMA, TIPO_ANUNCIO, LISTA_REPRODUCCION_VIDEO_ID," \
              "SPOTX_PISO_PRECIO_CENTAVOS, SPOTX_TIEMPO_ESPERA_CADUCA "\
              "FROM sitio_configuracion_video "\
              "WHERE SITIO_APLICACION_ID=%d" % (SITIO_APLICACION_ID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getSiteConfigurationSsp(self, SITIO_APLICACION_ID):
        cursor = self.conn.cursor()
        sql = "SELECT FORMATO, PARAMETRO, VALOR, TIPO_VALOR " \
              "FROM sitio_configuracion_ssp  " \
              "WHERE ACTIVO=b'1' AND SITIO_ID=%d" % (SITIO_APLICACION_ID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def getEtiquetaConfiguracionRelap(self, etiquetaID):
        cursor = self.conn.cursor()
        sql = "SELECT PARAMETRO, PLATAFORMA, VALOR, TIPO_VALOR " \
              "FROM etiqueta_configuracion_relap  " \
              "WHERE ACTIVO=b'1' AND ETIQUETA_ID=%d" % (etiquetaID)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def closeConn(self):
        try:
            self.conn.close()
            return "Cerrado conn"
        except:
            return "Cerrado conn previamente"
