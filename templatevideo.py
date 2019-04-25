#!/usr/bin/python3


class VTemplate(object):
    """docstring for template"""
    def __init__(self, uuid_name, tagsListWeb, tagsListMobile, uuidValue, blackList, tagListDisplay,
                 videoPlayer, googIma, companion, spotx, relapurl, appnexus, etiqueta_conf):
        self.uuid_name = uuid_name
        self.tagsListWeb = tagsListWeb
        self.tagsListMobile = tagsListMobile
        self.ssps = tagListDisplay
        self.impresion = "{mobile:" + str(uuidValue[11]) + ", desktop:" + str(uuidValue[4]) + "}"
        self.frecuencia = "{mobile:" + str(uuidValue[6]) + ", desktop:" + str(uuidValue[5]) + "}"
        self.blackList = blackList
        self.mode = uuidValue[9]
        self.videoPlayer = videoPlayer
        self.googima = googIma
        self.companion = companion

        self.programacion_anuncio = "true" if uuidValue[12] == b'\x01' else "false"
        self.posicion_anuncio = uuidValue[13]
        self.mapeo_anuncio = "true" if uuidValue[14] == b'\x01' else "false"

        self.spotx = spotx
        self.relapurl = relapurl
        self.safe_mode = "true" if uuidValue[15] == b'\x01' else "false"
        self.interactive = etiqueta_conf
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
        width = relappro.helpers.getSize(uuid, mode, "width"),
        height = relappro.helpers.getSize(uuid, mode, "height"),
        url = relappro.helpers.getLocation(false, uuid, true),
        urlencode = relappro.helpers.getLocation(true, uuid, true),
        random = relappro.helpers.getRandom(),
"""
        template = template + "        videoPlayer = " + str(self.videoPlayer) + ";"
        template += """
    var randomItemVideo = relappro.helpers.getRandomItem(videoPlayer);
    var datos = {
        uuid: uuid,
        """
        template = template + "impresion: " + str(self.impresion) + ","
        template += """
        config: {
            videoClient: false,
        """

        template = template + " " * 4 + "googima: " + self.googima + ","
        template += """
            mode: mode,
        """
        template = template + " " * 4 + "frecuencia: " + str(self.frecuencia) + ","
        template += """
            gpt: {
"""
        template = template + " " * 16 + "mapping: " + self.mapeo_anuncio + ","
        template += """
                amazonps: true,
        """
        template = template + " " * 8 + str(self.companion)
        template += """
            },
"""
        template = template + " " * 12 + "adPosition: \"" + str(self.posicion_anuncio) + "\",\n"
        template = template + " " * 12 + "schedule: " + self.programacion_anuncio + ",\n"
        template = template + " " * 12 + "safemode: " + self.safe_mode + ",\n"
        template = template + " " * 12 + "interactive: " + self.interactive + ",\n"
        template = template + " " * 12 + "relapurl: \"" + str(self.relapurl) + "\",\n"
        template = template + " " * 12 + "spotx: " + self.spotx + ",\n"
        template = template + " " * 12 + "appnexus: " + self.appnexus + ","
        template += """
            dropdown: false
        },
        randomItemVideo: randomItemVideo,
        site: {
            encode: urlencode,
            unencode: url,
        """
        template = template + "    blackList: " + str(self.blackList) + ","
        template += """
        },
        tags: {
            video: {
        """
        template = template + " " * 8 + "mobile: " + self.tagsListMobile + ",\n"
        template = template + " " * 16 + "desktop: " + self.tagsListWeb
        template += """
        },
            display:
        """
        template = template + " " * 8 + str(self.ssps)
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
