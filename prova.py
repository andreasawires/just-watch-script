from justwatch import JustWatch
import pandas as pd

###CREAZIONE DATASET DI TEST
test_data = {"Titolo Film":["After We Fell", "Dark Blood", "The Hunting", "The Desperate Hour", "Titanic 666"], "TMBD_ID":[744275, 845885, 870671, 764835, 945657]}
df = pd.DataFrame(test_data)

###IMPORTO MODULO
just_watch = JustWatch(country="US")
dati_test = []

###Per ciascun elemento del dataset di film
for x in range(len(df.index)):

    tmb_id = df["TMBD_ID"][x] ##CAMBIA: tmdb id del film
    lista_providers = ["nfx", "amz"] ##CAMBIA: providers da cercare
    titolo_film = df["Titolo Film"][x] ##CAMBIA: titolo testuale del film

    results_by_providers = just_watch.search_for_item(query=titolo_film, providers=lista_providers) ##Output di tutti i film che assomigliano al titolo
    tutti_i_film = [film for film in results_by_providers["items"]] ##Array contenente tutti i film trovati, ma divisi uno ad uno

    ###Cerco di vedere se è il film univoco che sto cercando o no
    for movie in tutti_i_film:

        #Se contiene scoring (dati che a me interessano...alcuni film non hanno tali dati)
        if "scoring" in movie:
            lista_che_contiene_id = [item for item in movie["scoring"] if item["provider_type"] == "tmdb:id"]
            if lista_che_contiene_id:
                id_del_film_trovato = lista_che_contiene_id[0]["value"]
                if id_del_film_trovato == tmb_id:
                    film_data = movie
                    dati_test.append(film_data)
                    break

            else:
                continue
        else:
            dati_test.append("---NOT FOUND---")
            continue
        
    if dati_test:
        if dati_test[-1]["id"] != movie["id"]:
            dati_test.append("---NOT FOUND---")

print(dati_test)