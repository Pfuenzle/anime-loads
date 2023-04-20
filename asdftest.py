from animeloads import animeloads

#TODO download staffel

al = animeloads()

anime = al.getAnime("https://www.anime-loads.org/media/heion-sedai-no-idaten-tachi")


print(anime.downloadEpisode(1, anime.getReleases()[1], animeloads.UPLOADED, animeloads.CHROME))