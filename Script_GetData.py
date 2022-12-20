from justwatch import JustWatch
import pandas as pd

###CREAZIONE DATASET DI TEST
test_data = {"Titolo Film":["After We Fell", "Dark Blood", "The Hunting", "The Desperate Hour", "Titanic 666"], "TMBD_ID":[744275, 845885, 870671, 764835, 945657]}
df = pd.DataFrame(test_data)

###DATASET OUTPUT
data_output = {}

###IMPORTO MODULO
just_watch = JustWatch(country="US")
dati_test = []

###Per ciascun elemento del dataset di film
for x in range(len(df.index)):
    providers = {}
    film_detail = {}

    tmdb_id = df["TMBD_ID"][x] ##CAMBIA: tmdb id del film
    lista_providers = ["nfx", "amz", "amp", "dnp", "atp", "itu", "fuv"] ##CAMBIA: providers da cercare
    titolo_film = df["Titolo Film"][x] ##CAMBIA: titolo testuale del film

    results_by_providers = just_watch.search_for_item(query=titolo_film, providers=lista_providers) ##Output di tutti i film che assomigliano al titolo
    tutti_i_film = [film for film in results_by_providers["items"]] ##Array contenente tutti i film trovati, ma divisi uno ad uno

    ###Cerco di vedere se è il film univoco che sto cercando o no

    ###QUESTO RIGUARDA LA RICERCA DI UN SOLO FILM (paragono ogni film nella lista al film che mi interessa per vedere se c'è)
    for movie in tutti_i_film:
        backup_film = movie
        #Se contiene scoring (dati che a me interessano...alcuni film non hanno tali dati)
        if "scoring" in movie:
            lista_che_contiene_id = [item for item in movie["scoring"] if item["provider_type"] == "tmdb:id"]
            if lista_che_contiene_id:
                id_del_film_trovato = lista_che_contiene_id[0]["value"]
                #Se è il film che mi interessa:
                if id_del_film_trovato == tmdb_id:
                    film_data = movie
                    break

            else:
                continue
        else:
            continue
    
    #per non causare errore all'inizio
    if film_data:
        if film_data["id"] != backup_film["id"]: #Se la ricerca del film non ha avuto un buon esito (ultimo film cercato != da film voluto)
            film_data=""
        if film_data:
            try:
                offerte_film = film_data["offers"]
                offerte_film_interessanti = [x for x in offerte_film if x['provider_id'] in (8, 9, 337, 350, 2, 257)]
                providers_already_used = []
                offerte_finali = []
                for offer in offerte_film_interessanti:
                    if offer['package_short_name'] not in providers_already_used:
                        providers[offer['package_short_name']] = offer["urls"]["standard_web"]
                        providers_already_used.append(offer['package_short_name'])
                
            except:
                print("problem")
                offerte_finali = []
                pass

            id_justwatch = film_data["id"]
            film_title = film_data["title"]
            film_detail["Title"] = film_title
            film_detail["tmdb_id"] = tmdb_id
            film_detail["providers"] = providers
            data_output[id_justwatch] = film_detail
        
        
print(data_output)

    

