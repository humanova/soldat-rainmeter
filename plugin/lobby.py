import requests
import winsound

can_beep = True
# if any player in tracking list is found playing in a server, script will beep and notify
tracking_list = ['Example']

SERVERS_API_URL = "http://api.soldat.pl/v0/servers"
SERVER_API_URL = "http://api.soldat.pl/v0/server"

def getCurrentPlayers():
    r = requests.get(SERVERS_API_URL, params={"empty" : "no" , "bots" : "no"})
    data = r.json()
    
    servers = []
    server_players = []

    for entry in data["Servers"]:
        servers.append((entry["IP"], entry["Port"], entry['Name']))
    
    for server in servers:
        r = requests.get(f"{SERVER_API_URL}/{server[0]}/{server[1]}/players")
        data = r.json()
        pl_data = {"server" : server[2], "players" : data["Players"]}
        server_players.append(pl_data)  

    return server_players

if __name__ == "__main__":

    srv_info = getCurrentPlayers()
    print(srv_info)
    log_file = open("log.txt", "w+", encoding='utf-8')
    for srv in srv_info:
        log_file.write(f"!! {srv['server']}-{len(srv['players'])}\n")
        for p in srv['players']:
            log_file.write(f"  +{p}\n")
            if p in tracking_list:
                if can_beep:
                    winsound.Beep(2500, 600)