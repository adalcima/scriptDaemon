#!/usr/bin/python3


class DTemplate(object):
    """docstring for template"""
    def __init__(self, uuid_name, uuidValue, blackList, tagListDisplay, relapurl, appnexus):
        self.uuid_name = uuid_name
        self.ssps = tagListDisplay
        self.impresion = "{mobile:" + str(uuidValue[11]) + ", desktop:" + str(uuidValue[4]) + "}"
        self.frecuencia = "mobile ? " + str(uuidValue[6]) + " : " + str(uuidValue[5])
        self.blackList = blackList
        self.mode = uuidValue[9]

        self.programacion_anuncio = "true" if uuidValue[12] == b'\x01' else "false"
        self.posicion_anuncio = uuidValue[13]
        self.mapeo_anuncio = "true" if uuidValue[14] == b'\x01' else "false"

        self.relapurl = relapurl
        self.safe_mode = "true" if uuidValue[15] == b'\x01' else "false"
        self.appnexus = appnexus

    def createTemplate(self):
        template = """/*!
*RelapPro Publisher Tag v2.1.0 (https://app.relappro.com)
 *Copyright 2017-2028 | The relaploader Authors
*/
function uuidObject() {
"""
        template = template + "    var uuid = \"" + self.uuid_name + "\",\n"
        template = template + "        mode = \"" + str(self.mode) + "\","
        template += """
        relappro = new window.relappro(),
        url = relappro.helpers.getLocation(false, uuid, true),
        urlencode = relappro.helpers.getLocation(true, uuid, true);
    var datos = {
        uuid: uuid,
        """
        template = template + "impresion: " + str(self.impresion) + ","
        template += """
        config: {
            mode: mode,
            frecuencia: {
                    mobile:1.0,
                    desktop: 1.0
            },
            gpt: {
"""
        template = template + " " * 16 + "mapping: " + self.mapeo_anuncio + ","
        template += """
                amazonps: true
            },
"""
        template = template + " " * 12 + "adPosition: \"" + str(self.posicion_anuncio) + "\",\n"
        template = template + " " * 12 + "schedule: " + self.programacion_anuncio + ",\n"
        template = template + " " * 12 + "appnexus: " + self.appnexus + ",\n"
        template = template + " " * 12 + "safemode: " + self.safe_mode + ",\n"
        template = template + " " * 12 + "relapurl: \"" + str(self.relapurl) + "\""
        template += """
        },
        site: {
            encode: urlencode,
            unencode: url,
        """
        template = template + "    blackList: " + str(self.blackList) + ","
        template += """
        },
        tags: {
            display:
        """
        template = template + " "*12 + str(self.ssps)
        template += """
        },
        extra: {
            v: "2.1.0"
        }
    };
    this.get = function() {
        return datos;
    }
}
        """

        return template
