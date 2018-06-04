from flask import Flask, request, jsonify, Response
import json
import sqlite3 as sqlite
import configparser
import random
import requests
app = Flask(__name__)



@app.route('/<string:user>', methods=['GET'])
def getDragonColour(user):
    #set variables
    user.capitalize()
    type = ""
    lair = "Simple Cave"

    #load config values
    config = configparser.ConfigParser()
    config.read('../config/config.ini')
    twitchclientid = config['DEFAULT']['CLIENTID']
    twitchauthorization = config['DEFAULT']['AUTH']
    #print(config.sections())
    #twitchclientid = config.get('DEFAULT','CLIENTID')
    #twitchauthorization = config.get('DEFAULT','AUTH')


    #perform operations
    conn = sqlite.connect('../data/dragons.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE name =  ?", (user,))
    data=cur.fetchone()
    if data is None:
        #get id
        cur.execute("SELECT id FROM users WHERE id = (SELECT MAX(id) FROM users)")
        id = cur.fetchone()[0]
        id += 1
        #get twitch id
        url="https://api.twitch.tv/helix/users?login=" + user
        headers = {
        'client-id': twitchclientid,
        'Authorization': 'Bearer ' + twitchauthorization
        }
        response = requests.get(url, headers=headers).content
        jsondata = json.loads(response.decode('utf-8'))
        twitchid = jsondata["data"][0]["id"]
        #get type
        random.seed(twitchid)
        randval = random.randint(0,11)
        colours = ["Green", "Blue", "White", "Black", "Red", "Gold", "Bronze", "Copper", "Silver", "Brass", "Faerie"]
        type = colours[randval]
        cur.execute("INSERT INTO users values(?,?,?,?,?,?,?,?)",(id,user,type,lair,"",0,0,0))
    cur.execute("SELECT type FROM users WHERE name = ?", (user,))
    colour=cur.fetchone()
    if colour is None:
        print("something went wrong")
        #return 'error'
        return Response('error', mimetype='text')
    else:
        #return colour
        return Response(colour, mimetype='text')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    




