// THEME ONLOAD FUNCTION

$( document ).ready(function() {
  if ( ["light", "dark", "discord"].includes( getCookie( "theme" ) ) ) {
    console.log( "%c Setting Theme To " + getCookie( "theme" ) , 'color: #0ff' );

    setTheme( getCookie( "theme" ) )
  }
});

function setTheme( theme ) {
  if ( theme === "dark" ) { // light = #FBAE3C dark = #001220
    $('body').css('background-color', '#001220'); // change bg color
    $('.top').css('background-color', '#FBAE3C'); // change wave color
    $('.wave').css('fill', '#FBAE3C'); // change wave color
    $('.introbutton').css('background-color', '#001220'); // change button color
    $('.introhead').css('color', '#001220'); // change introhead color
    $('.nametitle').css('color', '#001220'); // change nametitle color
    $('.introtext').css('color', '#001220'); // change introtext color
    $('.featurehead').css('color', 'white'); // change subtitle color
    $('.invitehead').css('color', 'white'); // change subtitle color
    $('.homeul').css('background-color', '#FBAE3C'); // change nav color
    $('.linkcog').css('color', '#001220'); // change nav cog color
    $(".linkcog").hover(function(){
      $(this).css("color", "#077bd9");
      }, function(){
      $(this).css("color", "#001220");
    });
  }
}
