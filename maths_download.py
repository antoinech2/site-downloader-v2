############################################
# INFORMATIONS / DESCRIPTION:
# Titre : Site Downloader v2
# Programme Python 3.10.1 (compatilité des versions antérieures non assurée)
# Auteur: Antoine CHEUCLE
# Encodage: UTF-8
# Licence: GNU General Public License 3.0 (licence libre)
# Version: Release 2.0.0
# GitHub Repository : https://github.com/antoinech2/site-downloader-v2
# Date : 20 juillet 2022
# Description: Télécharge les fichiers du site de Maths de la classe
# de MP du lycée Clemenceau.
############################################

import mechanize
import http.cookiejar as cookielib
import os
import re
from bs4 import BeautifulSoup

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_cookiejar(cj)

total_files = 140
traite = 0

def send_progress(name):
    print(f"Téléchargement en cours... Fichier {traite}/{total_files} ({round(traite/total_files*100,1)}%)  --->  {name}")

def __main__():
    global traite
    url = "http://philippe.skler.free.fr/"
    pages = ["Cours", "TD", "DS", "DM", "Colles", "Archives"]

    base_path = "Mathématiques"

    for cat in pages:
        br.open(url+cat.lower()+".htm")
        soup = BeautifulSoup(br.response().read(), 'html.parser')
        path = base_path +"/"+ cat
        if not os.path.isdir(path):
            os.makedirs(path)
        for node in soup.find_all('a', href = re.compile(".pdf")):
            name = node.parent.getText().lstrip()
            name = name.replace(":", "-")
            name = name.replace("\xa0", "")
            name = name.replace("/", "")
            name = name.replace("?", "")

            url_link = node.get("href")
            link = br.find_link(url = url_link)
            if not link.text == "correction":
                name = name.replace("correction", "")
            try:
                br.retrieve(link.absolute_url, f"{path}/{name}.pdf")
            except:
                print(f"Erreur 404 : Fichier introuvable : {link.absolute_url}")
            traite += 1
            send_progress(name)

    print(f"Téléchargement terminé dans le dossier 'Mathématiques' !")

__main__()