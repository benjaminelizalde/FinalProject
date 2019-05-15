var cookies = 0;
var cookiesPerSecond = 0;
var cookiesPerClick = 1;
var cursorsOwned = 0;
var costOfCursors = 10;
var costOfCursorsMultiplier = 1;
var cursorWeight = 1;

var start = new Date;

//====================================================================================================

$(document).ready(function() {

//====================================================================================================

    function displayText()
    {
      $("#cookies").text(cookies);
      $("#cookiesPerSecond").text(cookiesPerSecond);
      $("#cookiesPerClick").text(cookiesPerClick);

    }

//===================================================================================================



//====================================================================================================

displayText();

//====================================================================================================

setInterval(function()
 {

    displayText();
    cookies = cookies + cookiesPerSecond;

  }, 1000);

//====================================================================================================

$("#cookie").click(function()
    {

      displayText();
      cookies = cookies + cookiesPerClick;


    });

//====================================================================================================

$("#save").click(function()
   {

      displayText();
      cookiesPerClick = cookiesPerClick + 1;

   });
//====================================================================================================

$("#cursor").click(function()
  {
    if(cookies >= costOfCursors)
    {
      displayText();
      cookiesPerSecond = cookiesPerSecond + cursorWeight;
      cookies = cookies - costOfCursors;
      cursorsOwned = cursorsOwned + 1;
      costOfCursors = costOfCursors * costOfCursorsMultiplier;
      costOfCursorsMultiplier = costOfCursorsMultiplier + cursorsOwned / 10;
      
    }
    else
    {
      alert("Insufficiant Cookies. You need " + (costOfCursors - cookies) + " more cookies to make that purchase");
    }



  });


});

//====================================================================================================
