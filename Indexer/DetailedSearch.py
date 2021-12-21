import re

replace = [[":", "."], [",", ""], ["!", ""]]

seasonSynonyms = ["Season", "S0"]
goodSeasonMappings = [["S01", "I", "Season 1", "Season 01", "S1", "1st", "first"], ["S02", "II", "Season 2", "Season 02", "S2", "2nd", "second"], ["S03", "III", "Season 3", "Season 03", "S3", "3rd", "third"], ["S04", "IV", "Season 4", "Season 04", "S4", "4th", "fourth"], ["S05", "V", "Season 5", "Season 05", "S5", "5th", "fifth"], ["S06", "VI", "Season 6", "Season 06", "S6", "6th", "sixth"], ["S07", "VII", "Season 7", "Season 07", "S7", "7th", "seventh"], ["S08", "VIII", "Season 8", "Season 08", "S8", "8th", "eigthth"], ["S09", "IX", "Season 9", "Season 09", "S9", "9th", "ninth"], ["S10", "X", "Season 10", "Season 10", "S10", "10th", "tenth"]]

def getSeason(synonyms=[], releaseTitle="", seriesName="", episode=-1):
    season = 1
    seasonString = "S01"
    if(len(synonyms) > 0 or seriesName != "" or releaseTitle != ""):
        for seasonMappings in goodSeasonMappings:
                for idx,mapping in enumerate(seasonMappings):
                    if(idx == 1):
                        continue
                    if(mapping.lower() in releaseTitle.lower() or mapping.lower() in seriesName.lower()):
                        try:
                            print("Found: " + mapping.lower() + " in " + releaseTitle.lower() + " or " + seriesName.lower())
                            return int(''.join(c for c in seasonMappings[0] if c.isdigit())), seasonMappings[0], True
                        except Exception as e:
                            print("Failed to parse season from series \"" + seriesName + " with synonyms \"" + str(synonyms))
                            return -1, "", False
                        break
                    for aniSyn in synonyms:
                        if(mapping.lower() in aniSyn.lower()):
                            try:
                                print("Found: " + mapping.lower() + " in " + aniSyn.lower())
                                return int(''.join(c for c in seasonMappings[0] if c.isdigit())), seasonMappings[0], True
                            except Exception as e:
                                print("Failed to parse season from series \"" + seriesName + " with synonyms \"" + str(synonyms))
                                return -1, "", False
                            break
    for syn in seasonSynonyms:
        for aniSyn in synonyms:
            if(syn in aniSyn):
                return -1, "", False
    return season, seasonString, False

class DetailedSearchRelease():

    def cleanReleaseTitle(self):
        releaseTitle = re.sub(
           r"Season 0|Staffel 0", 
           "S0", self.anmerkung)
        releaseTitle = re.sub(
           r"Season |Staffel ", 
           "S0", releaseTitle)
        return releaseTitle

    def createReleaseTitle(self):
        if(self.anmerkung != "" and ((self.group == "AST4u" or self.group == "Anime BluRay Junkies") and "." in self.anmerkung) and self.episode == -1):    #In der Beschreibung ausreichend benanntes Release
            self.releaseTitle = self.cleanReleaseTitle()
            self.releaseName = self.releaseTitle
            self.seasonInt = getSeason(self.synonyms, self.releaseTitle, self.series, self.episode)
            return
        
        groupPart  = "[" + self.group.replace("/", ".") + "]"

        if(self.episode != -1):
            episodeDot = ""
        else:
            episodeDot = "."

        if(self.anitype == "Movie"):
            episodeDot = "."
            seasonString = "." + str(self.year) + episodeDot
        elif(self.anitype == "OVA" or "OVA" in self.series.upper() or "OVA" in self.episodeName.upper()):
            episodeDot = "."
            OVAString = ".OVA."
            if "OVA" in self.series.upper():
                OVAString = "."
            seasonString = OVAString + str(self.year) + episodeDot
        else:    
            self.seasonInt, seasonString, goodSeason = getSeason(self.synonyms, "", self.series, self.episode)

            if(goodSeason):
                print("Found good season for " + self.series)

            seasonString = seasonString + episodeDot
        
            foundSeason = False

            skippableNames = ["season", "part", "teil"]
            if(self.series[-1].isnumeric()):
                nameSplit = self.series.split(" ")[:-1]
                newSeriesName = ""
                for namePart in nameSplit:
                    if(namePart.lower() in skippableNames):
                        continue
                    newSeriesName = newSeriesName + namePart + " "
                if goodSeason == False:
                    seasonString = "S0" + self.series[-1] + episodeDot
                    self.seasonInt = int(self.series[-1])
                    foundSeason = True
                    print("Found season in seriesname for " + self.series)
                self.series = newSeriesName

            elif(foundSeason == False and goodSeason == False):       #Fix for Danmachi
                lastName = self.series.split(" ")[-1]
                for idx,seasonMappings in enumerate(goodSeasonMappings):
                    if(foundSeason):
                        break
                    if(seasonMappings[1].lower() == lastName.lower()):
                        nameSplit = self.series.split(" ")[:-1]
                        newSeriesName = ""
                        for namePart in nameSplit:
                            if(namePart.lower() == "season"):
                                continue
                            newSeriesName = newSeriesName + namePart + " "
                        seasonString = seasonMappings[0] + episodeDot
                        self.seasonInt = idx+1
                        self.series = newSeriesName
                        foundSeason = True
                        print("Found roman numerals season in seriesname for " + self.series)
                        break

            isSpecial = False

            if(self.anitype == "Bonus"):
                isSpecial = True

            if(goodSeason == False):

                for syn in self.synonyms:
                    if("special" in syn.lower() or "bonus" in syn.lower()):
                       isSpecial = True

                if(isSpecial):
                    self.seasonInt = 0
                    seasonString = "S00" + episodeDot
            
            if(foundSeason == False):
                self.series = self.series + " "
            
        relTitle = re.sub('[^A-Za-z0-9 ]+', '.', self.series)
        
        relTitle = relTitle + seasonString
        
        if(self.episode != -1):
            relTitle = relTitle + "E" + str(self.episode).zfill(2) + " "
        if(self.episodeName != ""):
            for rep in replace:
                self.episodeName = self.episodeName.replace(rep[0], rep[1])
            relTitle = relTitle + self.episodeName + " "
        if(self.dubLang != "Japanese" and self.dubLang != ""):
            relTitle = relTitle + self.dubLang + " "
        else:
            relTitle = relTitle + self.subLang + " "
        audioformats = ["PCM", "FLAC", "DTS", "AC3", "AAC", "MP3"]
        for f in audioformats:
            if(f in self.anmerkung.upper()):
                relTitle = relTitle + f + " "
                break
        relTitle = relTitle + self.resolution
        if("bluray" in self.anmerkung.lower()):
            relTitle = relTitle + " BluRay"
        elif("web-rip" in self.anmerkung.lower() or "webrrip" in self.anmerkung.lower() or "web rip" in self.anmerkung.lower()):
            relTitle = relTitle + " Web-RIP"
        elif("web-dl" in self.anmerkung.lower() or "webdl" in self.anmerkung.lower() or "web dl" in self.anmerkung.lower() or "web" in self.anmerkung.lower()):
            relTitle = relTitle + " Web-DL"
        if("xvid" in self.anmerkung.lower()):
            relTitle = relTitle + " XVID"
        elif("x265" in self.anmerkung.lower()):
            relTitle = relTitle + " x265"
        elif("x264" in self.anmerkung.lower()):
            relTitle = relTitle + " x264"
        relTitle = relTitle + "-" + self.group            
        subdubPart = " ["
        for idx, d in enumerate(self.dubs):
            subdubPart  = subdubPart + d
            if(idx != (len(self.dubs) -1)):
                subdubPart = subdubPart + ","
        subdubPart  = subdubPart + "]"
        subdubPart  = subdubPart + "["
        for idx, s in enumerate(self.subs):
            subdubPart = subdubPart + s
            if(idx != (len(self.subs) - 1)):
                subdubPart = subdubPart + ","
        subdubPart  = subdubPart + "]"
        relTitle = relTitle.replace(" ", ".")
        while(".." in relTitle):
            relTitle = relTitle.replace("..", ".")
        if(self.episode == -1):
            episodesPart = " [" + str(self.curEpisodes) + " Episodes]"
        else:
            episodesPart = ""
        self.releaseName = relTitle
        self.releaseTitle = relTitle + subdubPart + episodesPart + " ["+ self.anitype + "]"
    
    def __init__(self, series, releaseID, anmerkung, group, resolution, dubLang, dubs, subLang, subs, size, url, curEpisodes, maxEpisodes, synonyms, anitype, year, episode=-1, episodeName=""):
        self.series = series
        self.releaseID = releaseID
        self.anmerkung = anmerkung
        self.group = group
        self.resolution = resolution
        self.dubLang = dubLang
        self.dubs = dubs
        self.subs = subs
        self.subLang = subLang
        self.size = size
        self.url = url
        self.curEpisodes = curEpisodes
        self.synonyms = synonyms
        self.anitype = anitype
        self.year = year
        self.maxEpisodes = maxEpisodes
        self.episode = episode
        self.episodeName = episodeName
        self.seasonInt = -1
        self.createReleaseTitle()
