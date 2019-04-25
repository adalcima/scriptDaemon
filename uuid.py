#!/usr/bin/python3

import re
import random
from database import DBase
from templatevideo import VTemplate
from templatedisplay import DTemplate
import urllib.parse


class UUID(object):
    """
    path: route in S.O. for saving created script files
    accessdb: access DB credentials
    """
    def __init__(self, path, accessdb):
        super(UUID, self).__init__()
        self.path = path
        self.db = DBase(accessdb)

    # Check for new requirements
    def req(self):
        return self.db.chekStatusUuid()

    # Change the status of the UUID
    def updateReq(self, status, etiqueta):
        return self.db.updateStatusUuid(status, etiqueta)

    # Close all DB connections
    def exit(self):
        return self.db.closeConn()

    # Process requests for building scripts
    def uuidManager(self, uuidValue):
        try:
            tagsListWeb = "["
            tagsListMobile = "["
            tagsList = {1: tagsListWeb, 2: tagsListMobile}
            blackList = []
            ad_tag_id = uuidValue[0]
            site_app_id = uuidValue[3]
            tag_format = uuidValue[8]

            # Get Google Ima configuration
            googImaConf = self.db.getSiteConfigurationVideo(site_app_id)
            if googImaConf[0][0] == b'\x01' and uuidValue[10] == "IMA":
                googIma = "{mobile: true, desktop: true}"
            else:
                googIma = "{mobile: false, desktop: false}"

            doubleclickExtra = googImaConf[0][1]
            spotx = "{floorPriceCents: " + str(googImaConf[0][3]) + ", " +\
                    "bidTimeout: " + str(googImaConf[0][4]) + "}"
            appnexus = self.appnexus_set_conf(site_app_id)
            relapurl = self.db.getRelapUrl(site_app_id)
            etiqueta_conf = self.etiqueta_set_conf(ad_tag_id)

            companion = ""
            if uuidValue[2]:
                companion = "companion: {propiedades: \"" + str(uuidValue[2]) + "\"}"

            # Get all scripts from etiqueta_publicitaria_ssp only for VIDEO
            # Fill tagsListWeb/tagsListMobile according to tag_type
            if tag_format == "VIDEO":
                total_ad_tag_scripts = self.db.getAdTagScript(ad_tag_id)
                for ad_tag_script in total_ad_tag_scripts:
                    script = ad_tag_script[0]
                    tag_type = ad_tag_script[2]  # TIPO (1 WEB, 2 MOBILE)
                    bid_apply = ad_tag_script[3]

                    # bid_apply for writting more than one request in tags
                    if bid_apply == b'\x01':
                        cpm = ad_tag_script[4]
                        cpm_dec = ad_tag_script[5]
                        cpm_min = ad_tag_script[6]
                        while (cpm >= cpm_min) and (cpm_dec > 0):
                            # tagsList[tag_type] = tagsList[tag_type] + self.tagParser(script, cpm, cpm_min)
                            tagsList[tag_type] = tagsList[tag_type] + "\"" + self.tagParser(
                                script, doubleclickExtra, cpm, cpm_min) + ","
                            cpm -= cpm_dec
                    else:
                        tagsList[tag_type] = tagsList[tag_type] + "\"" + self.tagParser(
                            script, doubleclickExtra) + ","

                tagsListWeb = tagsList[1][:-1] + "]"
                tagsListMobile = tagsList[2][:-1] + "]"

            # Fill blacklist
            total_blackList = self.db.getBlackList(site_app_id)
            for black in total_blackList:
                blackList.append(black[0])  # Add url to blacklist
            blackList = str(blackList)

            # Fill tagListDisplay with scripts in etiqueta_display_ssp
            total_display_tag_script = self.db.getDisplayTagScript(ad_tag_id)
            tagListDisplay = self.addSspDisplay(list(total_display_tag_script))

            # Define the script uuid file name
            uuid_name = uuidValue[1].replace("-", "")
            file = self.path + str(uuid_name) + ".js"

            # If there are video and display tags for VIDEO format
            print("taglistweb y taglistmobile")
            print(tagsListWeb)
            print(tagsListMobile)
            if len(tagsListWeb) > 3 and len(tagListDisplay) > 0 and tag_format == "VIDEO":
                videoPlayer = []
                if googImaConf[0][2]:
                    videoPlayer = self.videoPlayer(googImaConf[0][2])
                tagsListWeb = str(tagsListWeb).replace("\\", "")
                if len(tagsListMobile) > 1:
                    print("len mobile valida")
                    tagsListMobile = str(tagsListMobile).replace("\\", "")
                else:
                    print("igualar tags web y mobile")
                    tagsListMobile = tagsListWeb.replace("tagDesktop", "tagMobile")

                video_template = VTemplate(uuid_name, tagsListWeb, tagsListMobile, uuidValue, blackList, tagListDisplay,
                                           videoPlayer, googIma, companion, spotx, urllib.parse.quote_plus(relapurl[0]),
                                           appnexus, etiqueta_conf)
                template = video_template.createTemplate()
                with open(file, 'w') as fopen:
                    if fopen.write(template):
                        self.updateReq(2, ad_tag_id)
                        print(file)

            # If there are display tags for DISPLAY format
            elif len(tagListDisplay) > 0 and tag_format == "DISPLAY":
                display_template = DTemplate(uuid_name, uuidValue, blackList, tagListDisplay,
                                             urllib.parse.quote_plus(relapurl[0]), appnexus)
                template = display_template.createTemplate()
                with open(file, 'w') as fopen:
                    if fopen.write(template):
                        self.updateReq(2, ad_tag_id)
                        print(file)

            # Set stastus = 3 when no display tags
            elif (not tagListDisplay):
                print("No existe display")
                self.updateReq(3, ad_tag_id)

            else:
                print(uuidValue)
                print(total_ad_tag_scripts)
        except:
            print("uuidManager Error")

    def videoPlayer(self, LISTA_REPRODUCCION_VIDEO_ID):
        video_elements = []
        configurations = self.db.getVideo(LISTA_REPRODUCCION_VIDEO_ID)
        for conf in configurations:
            title = "title: \"" + conf[0] + "\""
            poster = "poster: \"" + conf[1] + "\""
            description = "description: \"" + conf[2] + "\""
            urldescription = "urldescription: \"" + urllib.parse.quote_plus(conf[3]) + "\""
            video = "video: \"" + conf[4] + "\""
            logo = "logo: \"" + conf[5] + "\""
            url= "url: \"" + conf[6] + "\""
            text = "text: \"" + conf[7] + "\""

            copyright_video = "copyright: {" + logo + ", " + url + ", " + text + "}"
            element = "{" + title + ", " + poster + ", " + description + ", " + \
                      urldescription + ", " + video + ", " + copyright_video + "}"

            video_elements.append(element)
        return str(video_elements).replace("'", "")

    # Create an empty script
    def createEmpty(self, uuidValue):
        template = """/*!
*Relapproads v1.3.0 (https://beta.relappro.com)
*Copyright 2017-2028 The relaploader Authors
*/
"""
        uuid_name = uuidValue[1].replace("-", "")
        file = self.path + str(uuid_name) + ".js"
        with open(file, 'w') as fopen:
            if fopen.write(template):
                self.updateReq(6, uuidValue[0])
                print(file)
        pass

    # Parse content from scripts, removing somo strings according to SSP
    def tagParser(self, tag, doubleclickExtra, cpm=0, cpm_min=0):
        r = random.uniform(0, 1)
        if tag.find("pubmatic.com") > 0:
            tag = re.sub(r"\player_height", "\" + height + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\player_width", "\" + width + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\insert_encoded_pageurl_here", "\" + urlencode + \"", tag, flags=re.IGNORECASE)
            tag = tag + "\""

        elif tag.find("ads.adaptv.advertising.com") > 0:
            tag = re.sub(r"\[cache_breaker]", "\" + random + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\embedding_page_url", "\" + urlencode + \"", tag, flags=re.IGNORECASE)
            tag = tag + "&width=\"+width+\"&height=\"+height"

        elif tag.find("ads.contextweb.com") > 0:
            tag = re.sub(r"\[url]", "\" + urlencode + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\[cache_buster]", "\" + random + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\[width]", "\" + width + \"", tag, flags=re.IGNORECASE)
            tag = re.sub(r"\[height]", "\" + height", tag, flags=re.IGNORECASE)

        elif tag.find("doubleclick") > 0:
            tag = tag.replace("%%PATTERN:url%%", "\" + urlencode + \"")
            if tag.find("%%CACHEBUSTER%%") > 0:
                tag = tag.replace("%%CACHEBUSTER%%", "\" + random + \"")
                tag += "\""
            else:
                tag = tag + "&correlator=\" + random"

            if doubleclickExtra == "LINEAL":
                tag = tag + " + \"&vad_type=lineal\""
            elif doubleclickExtra == "UNLINEAR":
                tag = tag + " + \"&vad_type=nonlinear\""

        elif tag.find("s.richaudience.com") > 0:
            tag = re.sub(r"\[cachebuster]", "\" + random + \"", tag, flags=re.IGNORECASE)
        elif tag.find("servedby") > 0:
            # tag = tag.replace("[CACHE_BREAKER]", "\\%%CACHEBUSTER\\%%\"")
            tag = tag.replace("[CACHE_BREAKER]", "\" + random + \"")
            tag += "\""
        # tag = str("""\"%s\"""" % tag)
        return tag

    # Proccess the content for display
    def addSspDisplay(self, sspDisplay):
        # propertys_available = ('pubId', 'siteId', 'kadId', 'kadtype', 'kadpageurl')
        result = []
        sspIds = []
        for element in sspDisplay:
            ssp_id = element[0]
            if ssp_id in sspIds:
                pass
            else:
                sspIds.append(ssp_id)
                ssp_name = element[1].lower()
                ssp = "{ssp:'" + ssp_name + "'"
                for sub in sspDisplay:
                    if sub[0] == ssp_id:
                        # list_propertys = {}
                        # script = sub[2].split(";")
                        script = sub[2]
                        # for element in script:
                        #    if any(p in element for p in propertys_available):
                        #        element = element.split("=")
                        #        list_propertys.update([(element[0], element[1])])

                        tag_type = sub[3]  # TIPO (1 DESKTOP, 2 MOBILE)
                        width = sub[4]
                        height = sub[5]
                        if ssp_name == "pubmatic":
                            script = "{" + str(script) + ",kadtype: 1,kadpageurl: urlencode}"
                        else:
                            script = "'" + str(script) + "'"
                        size = "'" + str(width) + "x" + str(height) + "'"
                        # list_propertys = str(list_propertys).replace("'", "")
                        if tag_type == 1:
                            ssp = ssp + ", desktop:{propiedades:" + script + ", size: " + size + "}"
                        elif tag_type == 2:
                            ssp = ssp + ", mobile:{propiedades:" + script + ", size: " + size + "}"
                ssp = ssp + "}"
                result.append(ssp)

        print("ssp result ")
        result = str(result).replace('"', '')
        result = str(result).replace("'", "\"")
        print(result)
        return result

    def appnexus_set_conf(self, site_app_id):
        appnexus = []
        configurations = self.db.getSiteConfigurationSsp(site_app_id)
        for conf in configurations:
            element = conf[0].lower() + ": {" + conf[1] + ": " + str(conf[2]) + "}"
            appnexus.append(element)

        result = str(appnexus).replace("[", "{")
        result = str(result).replace("]", "}")
        result = str(result).replace("'", "")
        return result

    def etiqueta_set_conf(self, ad_tag_id):
        interactive = []
        configurations = self.db.getEtiquetaConfiguracionRelap(ad_tag_id)
        for conf in configurations:
            element = conf[1].lower() + ": " + conf[2]
            interactive.append(element)

        #list_variables = [] # [{interactive: {desktop: true, mobile: false}, {var2: {desktop: true, mobile: false}]
        result = str(interactive).replace("[", "{")
        result = str(result).replace("]", "}")
        result = str(result).replace("'", "")
        print(result)
        return result
