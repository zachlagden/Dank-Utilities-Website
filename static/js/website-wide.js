//                                                     COOKIE MESSAGE DISPLAY

$(document).ready(function() {
  if (getCookie("cookie_msg") != "false") {
    var el = document.getElementById("cookie");
    el.style.display = "flex";
  }
});

function close_cookie_message() {
  var el = document.getElementById("cookie");
  setTimeout(function(){ el.style.display = "none"; }, 100);
  document.cookie = "cookie_msg=false";
}

//                                                     ENABLE SMOOTHSCROLL

var scroll = new SmoothScroll('a[href*="#"]');

//                                                     IMPORTING BROWSER UPDATE TO ALL PAGES

var $buoop = {required:{e:-4,f:-3,o:-3,s:-1,c:-3},insecure:true,api:2021.05 };
function $buo_f(){
 var e = document.createElement("script");
 e.src = "//browser-update.org/update.min.js";
 document.body.appendChild(e);
};
try {document.addEventListener("DOMContentLoaded", $buo_f,false)}
catch(e){window.attachEvent("onload", $buo_f)}

//                                                     USEFULL FUNCIONS

// GET A COOKIE BY THE NAME

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// GET JSON RESPONCE FROM URL

function jsonHttpGetFrom(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    var raw_responce = xmlHttp.responseText;
    var json_responce = JSON.parse(raw_responce);
    return json_responce
}

// OPEN WINDOW IN MIDDLE OF PAGES

const popupCenter = ({
  url,
  title,
  w,
  h
}) => {
  //                                                       Most browsers       Firefox (for some dumb reason)
  const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
  const dualScreenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;

  const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
  const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

  const systemZoom = width / window.screen.availWidth;
  const left = (width - w) / 2 / systemZoom + dualScreenLeft
  const top = (height - h) / 2 / systemZoom + dualScreenTop
  const newWindow = window.open(url, title,
    `
    scrollbars=yes,
    width=${w / systemZoom},
    height=${h / systemZoom},
    top=${top},
    left=${left}
    `
  )
  if (window.focus) newWindow.focus();
}

// GET URL ARGS

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

function getParam(query) {
  return urlParams.get(query)
}

// GO BACK IN PAGE HISTORY

function goBack() {
  window.history.back()
}
