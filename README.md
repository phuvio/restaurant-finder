# Löydä ravintola -sovellus

Sovelluksen vaatimusmäärittely ja SQLskeema löytyvät:

- [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

## Valmis ohjelma

Ohjelmaa voi testata: [Löydä ravintola](https://tsoha2023-restaurant-finder.fly.dev/login)

Ohjelmaan voi luoda uusia käyttäjiä ja kirjautua sisään. Ohjelmaa voi käyttää rajoitetusti myös ilman kirjautumista.

Etusivulla on kartta, jossa tietokantaan luodut ravintolat näkyvät merkkeinä. Merkissä lukee kyseisen ravintolan nimi. Klikkaamalla merkkiä, sen yläpuolelle ilmestyy infolaatikko, jossa on ravintolan tähtien määrä sekä linkki ravintolan tietosivulle. Etusivulla voi myös hakea ravintoloita hakusanalla tai ryhmistä. Hakujen tulokset tulevat näkyviin sivun alaosaan. Klikkaamalla ravintolan nimeä siirrytään kyseisen ravintolan sivulle.

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
- siirto Fly.io:hon aiheutti sen, että Google maps ilmoittaa virheellisestä api key:stä. Kyseinen api key toimii kuitenkin lokaalisti.
- välillä tulee erikoisia virheilmoituksia - johtunee Fly.io:n tietokannan hitaudesta?
