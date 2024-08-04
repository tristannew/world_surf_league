import requests
import re
import ast

def popup_data_request(url:str, heat_id:str, rnd_id:str):

    response = _get_response(url=url, heat_id=heat_id, rnd_id=rnd_id)
    # nationality_pattern = r'<span class=\\"athlete-country-name\\">(.*?)<'
    # Returns list of tuples of mathces [(surfer, nation), (surfer, nation)]
    nationality_pattern = r'<div  class=\\"hot-heat-athlete__name hot-heat-athlete__name--full\\">(.*?)<.*?class=\\"athlete-country-name\\">(.*?)<'
    nationalities = re.findall(nationality_pattern, response.text)

    # There won't necessarily be a new line after the wave range div
    wave_range_pattern = r'<div class=\\"label\\">Wave range<\\/div>\\n                <div class=\\"value\\">(.*?)<'
    try:
        wave_range = re.findall(wave_range_pattern, response.text)[0]
    except:
        wave_range = None

    wind_pattern = r'<div class=\\"label\\">Wind conditions<\\/div>\\n                <div class=\\"value\\">(.*?)<'
    try:
        wind = re.findall(wind_pattern, response.text)[0]
    except:
        wind = None

    date_pattern = r'class=\\"post-event-watch-heat-details-header__title-meta-status post-event-watch-heat-details-header__title-meta-status--completed\\">Completed<\\/div><div>(.*?)<'
    try:
        date = re.findall(date_pattern, response.text)[0]
    except:
        date = None

    # Returns list of tuples of mathces [(surfer, score), (surfer, score)]
    heat_score_pattern = r'<div  class=\\"hot-heat-athlete__name hot-heat-athlete__name--full\\">(.*?)<.*?class=\\"hot-heat-athlete__score\\">(.*?)<'
    heat_scores = re.findall(heat_score_pattern, response.text)

    # Could also use dict comprehension and .split(":") the string
    data_dict = ast.literal_eval(re.findall(r'{\\"event\\".*?}', response.text)[0].replace("\\", ""))

    ######## CREATE UNIQUE IDS ########
    # Unique Heat ID
    heat_uid = date+data_dict["athlete_names"]+data_dict["round_numbers"]

    # Unique surfer id
    surfer_ids = {surfer_name: surfer_name.replace(" ", "").lower()+surfer_nation.replace(" ", "").lower()
                 for surfer_name, surfer_nation 
                 in nationalities}
    
    surfer_nations = {surfer_name: surfer_nation for surfer_name, surfer_nation
                      in nationalities}
    

    ####### SORT HEAT TOTALS #########

    heat_totals = {surfer_name: heat_total
                   for surfer_name, heat_total
                   in heat_scores}

    ## HEAT INFO - strings
    heat_info = {
        "heat_id":heat_uid,
        "round_num":data_dict["round_numbers"],
        "round_name":data_dict["round_names"],
        "gender":data_dict["tour_genders"],
        "event_name":data_dict["event_names"],
        "event_group_name":data_dict["event_group_names"],
        "wave_range":wave_range,
        "wind":wind,
        "date":date,
        "tour_code":data_dict["tour_codes"]
        }
    # data_dict["athlete_names"]

    scores_info = []
    for surfer_name, heat_total in heat_totals:
        row = {
        "heat_id": heat_uid,
        "surfer_id": surfer_ids[surfer_name],
        "name": surfer_name,
        "heat_total": heat_total,
        "nationality": surfer_nations[surfer_name]
        }
        scores_info.append(row)

    
    return heat_info, scores_info

def _get_response(url:str, heat_id:str, rnd_id:str):
    querystring = {
        # Heat Id is through the details link
        "heatId":heat_id,
        # rnd would be from the round button, although that doesn't seem to be the same as this?
        # "rnd":"1710407694914",
        "rnd":rnd_id,
        #
        "pbv":"f6553ddd62cd7f8bc717283057c80be775f2c719-7183",
        "requestName":"postEventWatchHeatDetailsPopup"
        }

    payload = ""
    headers = {
        "cookie": "locale=en_GB",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Ajax-Request": "postEventWatchHeatDetailsPopup",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "https://www.worldsurfleague.com/events/2023/ct/66/billabong-pro-pipeline/results",
        "Cookie": "locale=en_GB; wslui={%22rv%22:3%2C%22pv%22:1%2C%22cpvts%22:1710407647485%2C%22cc%22:%22GB%22}; _ga=GA1.2.496146763.1710407533; _gid=GA1.2.1640446163.1710407533; usprivacy=1---; _awl=2.1710407648.5-63161fb9d7c9f1eb9a55d095423419dc-6763652d6575726f70652d7765737431-0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+14+2024+09%3A14%3A46+GMT%2B0000+(Greenwich+Mean+Time)&version=202310.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=36639d75-4f6d-4941-851d-d226ea5758ec&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A1%2CC0001%3A1%2CC0005%3A1%2CC0003%3A1%2CV2STACK42%3A1&AwaitingReconsent=false; OneTrustWPCCPAGoogleOptOut=false; _gat=1; OptanonAlertBoxClosed=2024-03-14T09:14:46.676Z; eupubconsent-v2=CP7dmwAP7dmwAAcABBENArEsAP_gAEPgACiQg1NX_H__bW9r8Xr3aft0eY1P99j77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQFlHJDUTVigaogVryDMakWcgTNKJ6BkiFMRM2dYCF5vmQtj-QKY5vp9d3dx2D-t_dv83dzyz8VHn3e5_2e0eJCdA58tDfv9bROb-9IPd_58v4v0_F_rk2_eT1l_tevp7B8uft87_XU-9_fff79AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQqIA-yJCQi0HCKBACoKwgIoEAAAAJA0QEAJgwKdgYBLrCRACAFAAMEAIAAUZAAgAAEgAQiACQAoEAAEAgUAAIAAAgEADAwABgAtBAIAAQHQIUwIAFAsAEjMiIUwIQoEggJbKBBICgQVwgCLPAggERMFAAACQAVgACAsFgMSSAlYkECXEG0AABAAgEEIFQik6MAQwJmy1U4om0ZWkBYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_wACHwAAAAA; _ga_ZE6TW33RHV=GS1.1.1710407686.1.0.1710407686.0.0.0; seerses=e; seerid=4712879d-73d7-4dc7-85ae-be1382d462b1; _dc_gtm_UA-47826941-1=1; _gat_UA-47826941-21=1; __gads=ID=c031455346e7b188:T=1710407689:RT=1710407689:S=ALNI_MZ7x62fs53Qh0Kew7O7OyhalL35vQ; __gpi=UID=00000d453d31d380:T=1710407689:RT=1710407689:S=ALNI_Mal3NEo_7XVtfZ96zlHgofYdfaUjQ; __eoi=ID=aa4f735d2790c3ed:T=1710407689:RT=1710407689:S=AA-AfjagM0pxlBj1k2kDpOuH_Cdg; _fbp=fb.1.1710407689523.619937120",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response

def request_all_heats():
    url = "https://www.worldsurfleague.com/events/2023/ct/66/billabong-pro-pipeline/results"

    return None
    

    ## WAVE INFO - strings ## NOTE doing heat scores for now
    # wave_id = None
    # surfer_id = None
    # heat_id = None
    # heat_totals = None

    # wave_dictionaries = None # NOTE: this will end up being multiple rows of data with unique wave ids to be joined
    # with heat ids to get the surfers
    # wave_dictionaries format.....
    # [{"surfer_id":1234, "heat_id":1234, "wave_score":9.67, "scoring":True}, {}, {}]

    # heat_dictionaries = None # NOTE: this will end up being a row of data with a unique heat id, and each surfers id
    # heat_dictionary format
    # [{"heat_id":1234, "gender":"F", "tour":"MCT", "event_name":"pipe", "group_name":"blah", 
    # "round":Opening, "round":1, "date":1234, "wind":"calm", "waves":4-6}]
    






    # surfer_dictionaries = None
    # surfer_dictionaries format
    # [{"surfer_id":1234, "name":"Kelly", "country":"USA", "DOB":1234}] # NOTE: this will be scraped
    # in a separate dictionary