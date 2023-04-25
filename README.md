# Löydä ravintola -sovellus

Sovelluksen vaatimusmäärittely ja SQLskeema löytyvät:

- [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

## Välipalautus 3

Ohjelmaa voi testata: [Löydä ravintola](https://tsoha2023-restaurant-finder.fly.dev/login)

Ohjelmaan voi luoda uusia käyttäjiä ja kirjautua sisään. 

Etusivulla on kartta, jossa tietokantaan luodut ravintolat näkyvät merkkeinä. Merkissä lukee kyseisen ravintolan nimi. Klikkaamalla merkkiä, sen yläpuolelle ilmestyy infolaatikko, jossa on ravintolan tähtien määrä sekä linkki ravintolan tietosivulle. Etusivulla voi myös hakea ravintoloita hakusanalla tai ryhmästä. Klikkaamalla ravintolan nimeä siirrytään kyseisen ravintolan sivulle.

Ravintolan sivulla näkyy ravintolan tiedot ja kirjautunut käyttäjä voi jättää arvion ravintolasta.

Pääkäyttäjä pääsee hallinnoimaan tietokantaan tallennettuja tietoja. 

Pääkäyttäjä voi 
- lisätä ravintoloita
- poistaa ravintola näkyvistä
- palauttaa ravintola näkyviin
- poistaa ravintolalle annetun kommentin
- muuttaa ravintolan tietoja
- lisätä ryhmiä
- poistaa ryhmä näkyvistä
- palauttaa ryhmä näkyviin
- lisätä ravintola ryhmään
- poistaa ravintola ryhmästä
- poistaa perustason käyttäjän, jolloin myös käyttäjän kommentit poistetaan
- muuttaa käyttäjän roolia

Testausta varten uudet käyttäjät rekisteröityvät pääkäyttäjiksi.

## Tunnetut puutteet
- siirto Fly.io:hon rikkoi kartan eli se ei näy
  - ongelma on siinä, että käytin Flask GoogleMapsin versiota 0.4.1.1
  - PYPI:ssä on versio 0.4.1, jolla en saanut karttaa näkyviin
  - googlaamalla löytyi muitakin, joilla oli sama ongelma ja jotka olivat saaneet kartan näkyviin käyttämällä versiota 0.4.1.1
  - PYPI:ssä ei ole versiota 0.4.1.1 vaan se täytyy ladata käsin omalle koneella ja asentaa sieltä
  - kun deployaa buildin Fly.io:hon, niin se ei löydä oikeaa versiota eikä se osaa ladata tuota koneelta asennettua versiota 
  - jouduin siis peruuttamaan versioon 0.4.1, jolloin karttakin hävisi
- välillä tulee erikoisia virheilmoituksia - johtuuko tietokannan hitaudesta?
