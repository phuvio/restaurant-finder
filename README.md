# Löydä ravintola -sovellus

Sovelluksen vaatimusmäärittely ja SQLskeema löytyvät:

- [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

## Välipalautus 2

Ohjelmaa voi testata: [Löydä ravintola](https://tsoha2023-restaurant-finder.fly.dev/login)

Ohjelmaan voi luoda uusia käyttäjiä ja kirjautua sisään. 

Etusivulla on kartta, jossa tietokantaan luodut ravintolat näkyvät merkkeinä. Merkissä lukee kyseisen ravintolan nimi. Klikkaamalla merkkiä, sen yläpuolelle ilmestyy infolaatikko, jossa on ravintolan tähtien määrä sekä linkki ravintolan tietosivulle. Etusivulla voi myös hakea ravintoloita hakusanalla tai ryhmästä. Klikkaamalla ravintolan nimeä siirrytään kyseisen ravintolan sivulle.

Ravintolan sivulla näkyy ravintolan tiedot ja kirjautunut käyttäjä voi jättää arvion ravintolasta.

Pääkäyttäjä pääsee hallinnoimaan tietokantaan tallennettuja tietoja. 

Pääkäyttäjä voi 
- lisätä ravintoloita
- lisätä ryhmiä
- poistaa ryhmiä näkyvistä
- palauttaa ryhmiä näkyviin
- lisätä ravintoloita ryhmiin
- poistaa ravintoloita ryhmistä
- poistaa perustason käyttäjän, jolloin myös käyttäjän kommentit poistetaan
- muuttaa käyttäjän roolia

### Tunnetut puutteet

- sivun ulkoasu on tekemättä
- pääkäyttäjän ominaisuudet puuttuvat
  - ravintolan tietojen muokkaaminen
  - ravintolan poistaminen
  - kommenttien poistaminen 
