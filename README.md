# Löydä ravintola -sovellus

Sovelluksen vaatimusmäärittely ja SQLskeema löytyvät:

- [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

## Välipalautus 2

Ohjelmaa voi testata: [Löydä ravintola](https://tsoha2023-restaurant-finder.fly.dev/login)

Ohjelmaan on rakennettu perusominaisuudet. Pääkäyttäjän ominaisuudet puuttuvat, joten uusia ravintoloita ei voi lisätä eikä nykyisiä hallinnoida.

Ohjelmaan voi luoda uusia käyttäjiä ja kirjautua sisään. Etusivulla näkyy luettelo tietokantaan luoduista ravintoloista. Klikkaamalla ravintolan nimeä, saa näkyviin ravintolan tiedot. Sivulla kirjautunut käyttäjä voi jättää arvion ravintolasta.

### Tunnetut puutteet

- tietosuojaominaisuudet puuttuvat (sivuilla voi siirtyä myös ilman kirjautumista)
- etusivun kartta ei näy (siksi ravintolat ylhäällä listana)
- hakusana- tai ryhmähaku tuottaa luettelon, mutta luettelon ravintoloiden nimet eivät ole linkkejä
- pääkäyttäjän ominaisuudet puuttuvat
  - ravintolan lisääminen
  - ravintolan tietojen muokkaaminen
  - ravintolan poistaminen
  - ryhmän luominen
  - ravintoloiden lisääminen ja poistaminen ryhmästä
  - ryhmän poistaminen
  - kommenttien poistaminen
  - käyttäjien poistaminen
  - käyttäjien roolin muuttaminen 
 
