import os, json
from urllib.request import Request, urlopen
from urllib import parse

lol_apikey = os.getenv("API_KEY")
if not lol_apikey:
    json_data = open(os.getcwd() + "/token/.config.json", encoding='utf-8').read()
    config_json = json.loads(json_data)
    lol_apikey = config_json["riot_api_key"]

request_url = "https://kr.api.riotgames.com"
req_api_key = "?api_key=" + lol_apikey

    
class Summoner():

    def __init__(self, summoner_name):
        self.summoner_name = summoner_name
        self.account = self.get_summoner(summoner_name)
        self.account_id = self.account.get("accountId", "")
        self.summoner_id = self.account.get("id", "")
        self.summoner_info = self.get_summoner_info()
        self.recent_winning_rate = self.get_recent_winning_rate()
        

    def get_summoner_info(self):
        summoner_api_url = "/lol/league/v4/entries/by-summoner/"
        
        try:
            req = Request(request_url + summoner_api_url + self.summoner_id + req_api_key)
            res = urlopen(req).read().decode('utf-8')
        except:
            return [{"message":"없는 소환사입니다"}]
        info = json.loads(res)
        return info


    def get_summoner(self, name):
        account_api_url = "/lol/summoner/v4/summoners/by-name/"
        summoner_name = parse.quote(name)

        try:
            req = Request(request_url + account_api_url + summoner_name + req_api_key)
            res = urlopen(req).read().decode('utf-8')
        except:
            return {"none":"none"}
        
        summoner_info = json.loads(res)
        return summoner_info


    def get_match(self, game_id):
        match_api_url = "/lol/match/v4/matches/"
    
        req = Request(request_url + match_api_url + str(game_id) + req_api_key)
        res = urlopen(req).read().decode('utf-8')

        match = json.loads(res)
        return match


    def get_match_list(self):
        matches_api_url = "/lol/match/v4/matchlists/by-account/"
        end_index = "&endIndex=20"
        queue = "&queue=420"

        try:
            req = Request(request_url + matches_api_url + self.account_id + req_api_key + end_index + queue)
            res = urlopen(req).read().decode('utf-8')
        except:
            return []

        match_id_list = json.loads(res)["matches"]
        match_list = []
        for match_id in match_id_list:
            match = self.get_match(match_id["gameId"])
            if match["gameDuration"] > 600 :
                match_list.append(match)

        return match_list


    def get_recent_winning_rate(self):
        match_list = self.get_match_list()
        if not match_list:
            return 0
        win_number = 0
        for match in match_list:
            my_team = 0
            for participant in match["participantIdentities"]:
                if participant["player"]["accountId"] == self.account_id:
                    if participant["participantId"] > 5:
                        my_team = 1
                    else:
                        my_team = 0
            if match["teams"][my_team]["win"] == "Win":
                win_number = win_number + 1
    
        return win_number / len(match_list)

if __name__ == "__main__":
    summoner = Summoner(input())
    print(summoner.summoner_info)
    print(summoner.recent_winning_rate)