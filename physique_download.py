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
# Description: Télécharge les fichiers du site de Physique-Chimie de la classe
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

url = "https://cahier-de-prepa.fr/mp-clemenceau/docs?phys"

br.open(url)
br.select_form(nr=0)
br.form['login'] = input("Entrez votre identifiant 'Cahier de prépa'")
br.form['motdepasse'] = input("Entrez votre mot de passe 'Cahier de prépa'")
br.submit()
br.open(url)

a_traiter = []
total_files = 434
traite = 0

def add_links():
    for link in br.links(url_regex = "^\?"):
        a_traiter.append(link)

def download(path):
    global traite
    if not os.path.isdir(path):
        os.makedirs(path)
    soup = BeautifulSoup(br.response().read(), 'html.parser')
    for node in soup.find_all('a', href = re.compile("^download\?")):
        url = node.get("href")

        ext = re.search("\((\w+),", node.parent.findChildren("span", {"class" : "docdonnees"})[0].getText()).group(1)
        link = br.find_link(url = url)

        if ext in ["mp4","mov"]:
            br.follow_link(link)
            br.retrieve(br.find_link(url_regex="^download", nr=0).absolute_url, f"{path}{link.text}.{ext}")
            br.back()
        else:
            br.retrieve(link.absolute_url, f"{path}{link.text}.{ext}")

        traite += 1
        send_progress(link.text+'.'+ext)

def get_path():
    path = ""
    for link in br.links(url_regex = "^docs\?rep"):
        path += link.text + "/"
    return path

def send_progress(name):
    print(f"Téléchargement en cours... Fichier {traite}/{total_files} ({round(traite/total_files*100,1)}%)  --->  {name}")


def __main__():
    add_links()

    if len(a_traiter) == 0:
        print("Erreur d'identifiants. Ressayez.")
        return

    for link in a_traiter:
        br.follow_link(link)
        add_links()
        download(get_path())

    print(f"Téléchargement terminé dans le dossier 'Sciences Physiques' !")

__main__()