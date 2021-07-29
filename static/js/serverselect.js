//                                                     AUTO LIST RELOADING

var blurred = false;
window.onblur = function() {
  blurred = true;
};
window.onfocus = function() {
  blurred = false;
  setTimeout(function () {
    $('#guilds').load(document.URL +  ' #guilds');
  }, 5000);
};

//                                                     ADD BOT TO GUILD LINK FUNCTION

function addtoguild(id) {
  idstr = id.toString()

  popupCenter({
    url: "https://discord.com/api/oauth2/authorize?client_id=831647690106470420&permissions=8&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Faddreturn&scope=applications.commands%20bot&guild_id="+idstr,
    title: 'Add me to your server!',
    w: 550,
    h: 850
  });
}

//                                                     THEME ONLOAD FUNCTION

$( document ).ready(function() {
  if ( ["light", "dark", "discord"].includes( getCookie( "theme" ) ) ) {
    console.log( "%c Setting Theme To " + getCookie( "theme" ) , 'color: #0ff' );

    setTheme( getCookie( "theme" ) )
  }
});

function setTheme( theme ) {
  if ( theme === "dark" ) { // light = #FBAE3C dark = #001220
    $('body').css('background-image', 'url(/static?file=images/dark-serverselect-bg.svg)'); // change bg
    $('body').css('background-color', '#001220'); // change bg color
    $('.guildname').css('color', 'white'); // change guild's name color
    $('li a').css('color', '#001220'); // change nav text color
    $("li a").hover(function(){ // change nav text color (on hover)
      $(this).css("color", "#077bd9");
      }, function(){
      $(this).css("color", "#001220");
    });
  }
}
