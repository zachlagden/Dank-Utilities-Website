from flask import Flask, redirect, render_template, request, url_for, g, session, jsonify, send_file
from requests_oauthlib import OAuth2Session
import json, os, time, pymongo

OAUTH2_CLIENT_ID = "831647690106470420"
OAUTH2_CLIENT_SECRET = "nknoZ1iVHbJ27yrpNbX_nCADUWmdtXXf"
OAUTH2_REDIRECT_URI = 'http://localhost:5000/callback' #https://bobadankers.xyz//discord-callback http://localhost:5000/discord-callback

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

BOT_AUTH_KEY = "-iB&!K2$qMF$B{0D=:c[K{s2:]W=q3B4CLA=aAAoGLpP}U|xmS1eQ=IogPNsS:8hO!Kh<#VQX!7w*7VQyf1oqB8bv)AY!_#{TPP2P42:/lj_^MNe_2TrT+wk}k.244"

app = Flask(__name__)
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

#                 VARS/FUNCS/IFS

#MONGO DB

mongoclient = pymongo.MongoClient(
    "mongodb+srv://server:fjmZIeRJmidvj9KM@dank-memer-helper-bot.fciqp.mongodb.net/settings?retryWrites=true&w=majority")

#DISCORD 0AUTH2

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

#API CODES

api_codes = {
    "code_meanings": {
        "1": "OK",
        "100": "Invalid API Version",
        "101": "404: Not Found",
        "102": "401: Unauthorized",
        "103": "404: Guild Not Found",
        "104": "404: Guild Not Found In Database",
        "105": "401: Not Logged In",
    },
    "code_dicts": {
        "1": {"message": "OK", "code": 1},
        "100": {"message": "Invalid API Version", "code": 100},
        "101": {"message": "404: Not Found", "code": 101},
        "102": {"message": "401: Unauthorized", "code": 102},
        "103": {"message": "404: Guild Not Found", "code": 103},
        "104": {"message": "404: Guild Not Found In Database", "code": 104},
        "105": {"message": "401: Not Logged In", "code": 105},
    }
}

#                 MAIN PAGES

@app.route('/')
def home():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
        discrim = user["discriminator"]
        issignedin = True
    except:
        pfp = None
        name = None
        discrim = None
        issignedin = False

    userdata = {"pfp": pfp, "name": name, "discrim": discrim}

    return render_template("home.html", userdata=userdata, issignedin=issignedin)

@app.route('/settings')
def settings():
    return render_template("settings.html")

#                 SERVER SELECT

@app.route('/serverselect')
def serverselect():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        userguilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
    except:
        return redirect("/login")

    db = mongoclient["website"]
    dbguilds = db["guilds"]

    guilds = []
    db_guilds_in = []
    guilds_in = []
    guilds_not_in = []

    for guild_im_in in dbguilds.find({}):
        db_guilds_in.append(int(guild_im_in["_id"]))

    for guild in userguilds:
        if (guild["permissions"] & 0x8) == 0x8:
            try:
                if "a_" in guild["icon"]:
                    pfp = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild['icon'] + '.gif'
                else:
                    pfp = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild['icon'] + '.jpg'
            except:
                pfp = "https://discordapp.com/assets/322c936a8c8be1b803cd94861bdfa868.png"

            if int(guild["id"]) in db_guilds_in:
                guilds_in.append({"id": guild["id"], "data": guild, "am_i_in": True, "pfp": pfp})
            else:
                guilds_not_in.append({"id": guild["id"], "data": guild, "am_i_in": False, "pfp": pfp})

    for guild in guilds_in:
        guilds.append(guild)

    for guild in guilds_not_in:
        guilds.append(guild)

    return render_template("serverselect.html", guilds=guilds)

#                 DASHBOARD

@app.route('/dashboard/<id>')
def dashboard(id):
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        userguilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
    except:
        return redirect("/login")

    guilds_info = {}

    for guild in userguilds:
        if (guild["permissions"] & 0x8) == 0x8:
            try:
                if "a_" in guild["icon"]:
                    pfp = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild['icon'] + '.gif'
                else:
                    pfp = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild['icon'] + '.jpg'
            except:
                pfp = "https://discordapp.com/assets/322c936a8c8be1b803cd94861bdfa868.png"

            guilds_info[guild["id"]] = {"name": guild["name"], "pfp": pfp, "id": guild["id"]}

    return render_template("dashboard.html", guilds_info=guilds_info)

#                 WEBSITE API

@app.route('/api/<version>')
def api_version_check(version):
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        userguilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
    except:
        return jsonify(api_codes["code_dicts"]["105"])

    return jsonify(api_codes["code_dicts"]["101"])

@app.route('/api/<version>/<type>')
def api_v1(version, type):
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        userguilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
    except:
        return jsonify(api_codes["code_dicts"]["105"])

    authedguilds = []
    allguilds = []

    for guild in userguilds:
        allguilds.append(guild["id"])
        if (guild["permissions"] & 0x8) == 0x8:
            authedguilds.append(guild["id"])

    if version not in ["v1"]:
        return jsonify(api_codes["code_dicts"]["101"])

    if version == "v1":
        if type not in ["getserversettings"]:
            return jsonify(api_codes["code_dicts"]["100"])

        else:
            if request.args.get("guild_id") not in allguilds:
                return jsonify(api_codes["code_dicts"]["103"])

            if request.args.get("guild_id") not in authedguilds:
                return jsonify(api_codes["code_dicts"]["102"])

            db = mongoclient["settings"]
            dbsettings = db["main_settings"]

            if type == "getserversettings":
                guild_id = request.args.get('guild_id')
                servers_settings = dbsettings.find_one({"_id": int(guild_id)})
                if servers_settings != None:
                    return jsonify({"message": "OK", "json": servers_settings, "code": 1})
                else:
                    return jsonify(api_codes["code_dicts"]["104"])

#                 DISCORD 0AUTH2

@app.route('/login')
def login():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        name = user["username"]
        return redirect("/serverselect")
    except:
        issignedin = False

    scope = request.args.get(
        'scope',
        'identify email guilds')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    try:
        if request.values.get('error'):
            return request.values['error']
        discord = make_session(state=session.get('oauth2_state'))
        token = discord.fetch_token(
            TOKEN_URL,
            client_secret=OAUTH2_CLIENT_SECRET,
            authorization_response=request.url)
        session['oauth2_token'] = token
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()

        return redirect("/serverselect"), 302
    except:
        return render_template('errors/500.html'), 500

@app.route('/addreturn')
def addreturn():
    print(request.cookies)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

#                 CUSTOM ERROR PAGES

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('errors/500.html')

#                 STAIC FILES SERVING

@app.route('/static')
def static_request():
    file = request.args.get('file')
    try:
        return send_file(f'static/{file}', attachment_filename=file)
    except:
        return "404 - File not found!", 404


if __name__ == "__main__":
    app.run(debug=True)
