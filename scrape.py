from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
from datetime import date
import json
from standings import Team, Match, Score, Championship

def __set_headers(request):
    request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
    request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    request.add_header("Accept-Encoding","gzip, deflate, br")
    request.add_header("Accept-Language","en-US,en;q=0.9,it;q=0.8")
    request.add_header("Connection","keep-alive")
    request.add_header("Cookie","PHPSESSID=6k0ef1ai4lnmkhfvbaod8d7k67")
    request.add_header("Host","www.fipavonline.it")

def scrape(url):
    request = Request(url)
   
    __set_headers(request)
   
    html = urlopen(request).read()
    soup = BS(html, features="html.parser")

    matches_html = soup.find_all("div", attrs={"class":"risultati"})

    torneo = Championship(str(date.today()))

    for match_html in matches_html:
        gara = match_html.find("div", attrs={"class":"info-gara-data"}).contents[0].strip()
        giornata = match_html.find("div", attrs={"class":"info-gara-giornata"}).contents[0].strip()
        locali =  match_html.find("div", attrs={"class":"sq casa"}).find("span", attrs={"class":"sq-nLong"}).contents[0].strip()
        ospiti  = match_html.find("div",attrs={"class":"sq fuori"} ).find("span", attrs={"class":"sq-nLong"}).contents[0].strip()
        risultato  = match_html.find("span",attrs={"class":"s-scoreText risultato-ufficiale"} )
        
        if not risultato:
            risultato = match_html.find("span",attrs={"class":"s-scoreText"} )
        risultato = risultato.contents[0].strip()
        
        
        if risultato != "-":
            print(f"Gara {giornata} giocata")
            
            punti = risultato.split("-")
            punti_locali = int(punti[0])
            punti_ospiti = int(punti[1])

            localTeam = Team(locali)
            ospitiTeam  = Team(ospiti)
            score = Score(punti_locali,punti_ospiti)
            match = Match(localTeam,ospitiTeam,score,gara,giornata)

            torneo.add_match(match)
            
        else:
            print(f"gara tra {locali} e {ospiti} non ancora giocata")
    return torneo

def main():
    champ = scrape("https://www.fipavonline.it/main/gare_girone/47101/1")
    with open("campionato.json", "w") as out_file: 
        json.dump(champ.to_json(),indent=True, fp= out_file)
    
    with open("stats.json", "w") as out_file: 
        json.dump(champ.stats(),indent=True, fp= out_file)
    
if __name__ == "__main__":
    main()