// THEME ONLOAD FUNCTION (SPECIAL FOR SETTINGS)

$( document ).ready(function() {
  if ( ["light", "dark", "discord"].includes( getParam( "theme" ) ) ) {
    console.log( "%c Setting Theme Cookie To " + getParam( "theme" ) , 'color: #0ff' );

    document.cookie = "theme=" + getParam( "theme" );

    window.history.replaceState({}, '','/settings');
  }

  if ( ["light", "dark", "discord"].includes( getCookie( "theme" ) ) ) {
    console.log( "%c Setting Theme To " + getCookie( "theme" ) , 'color: #0ff' );

    setTheme( getCookie( "theme" ) )
  }
});

function setTheme( theme ) {
  if ( theme === "dark" ) { // light = #FBAE3C dark = #001220
    $('body').css('background-image', 'url(/static?file=images/dark-settings-bg.svg)'); // change bg
    $('.title').css('color', '#001220'); // change title color
    $('.form_text').css('color', '#001220'); // change form text color
    $('.fa-arrow-left').css('color', '#001220'); // change nav cog color
    $(".fa-arrow-left").hover(function(){
      $(this).css("color", "#077bd9");
      }, function(){
      $(this).css("color", "#001220");
    });
  }
}
