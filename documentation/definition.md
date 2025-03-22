## Määrittelydokumentti

- Opinto-ohjelma: TKT

- Dokumentaation kieli: suomi

- Ohjelman kieli: Python

- Muut kielet: Rust, Typescript

- Algoritmit: Fortunen algoritmi, ???

- Ongelma: Karttageneraatio on yleinen probleema esimerkiksi videopeleissä, jossa halutaan ikuisesti kasvava maailma. Karttagenerointia voi käyttää myös työkaluna tarinankerronnassa.

- Syötteet: Syötteitä ovat: solmujen määrä, kartan koko, ???

- Aikavaativuus: O(n log n)

- Lähteet: [https://en.wikipedia.org/wiki/Fortune%27s_algorithm](https://en.wikipedia.org/wiki/Fortune%27s_algorithm), [https://jacquesheunis.com/post/fortunes-algorithm/](https://jacquesheunis.com/post/fortunes-algorithm/)

## Ydin

Ohjelman ytimessä tulee olemaan Fortunen algoritmi. Fortunen algoritmi jakaa pinnan erikokoisiin alueihin pisteiden avulla siten, että jokaisen pisteen alueella on vain alue, joka on lähinnä juuri sitä pistettä. Tämä luo eri mallisia ja kokoisia alueita, joista voi muodostaa vaikka mantereita tai biomeja.

Algoritmi toimii swipeemällä läpi alueen siten, että alue generoituu sitä mukaan. Siihen tarvitaan paraabelejä ja reunantapausten löytämisen.
