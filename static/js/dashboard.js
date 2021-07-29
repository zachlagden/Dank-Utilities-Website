//          SETTING GLOBAL VARS

var global_url = window.location.href
var global_url_chunks = global_url.split("/")
var global_guild_id = global_url_chunks[4]

//          ON START

$(document).ready(function() {
  var server_settings = jsonHttpGetFrom("http://localhost:5000/api/v1/getserversettings?guild_id="+global_guild_id)
  document.getElementById("datatext").innerHTML = server_settings["json"]["commands"]["heist_ban"]["ban_reason"];
});
