var costOfCursorsMultiplier = 1;
var cursorWeight = 1;
var costOfGrandmasMultiplier = 1;
var grandmaWeight = 2;


var start = new Date;

//====================================================================================================

$(document).ready(function() {

//====================================================================================================

    function displayText()
    {
      $("#cookies").text(cookies);
      $("#cookiesPerSecond").text(cookiesPerSecond);
      $("#cookiesPerClick").text(cookiesPerClick);
      $("#cursorsOwned").text(cursorsOwned);
      $("#costOfCursors").text(costOfCursors);
      $("#grandmasOwned").text(grandmasOwned);
      $("#costOfGrandmas").text(costOfGrandmas);
    }

//===================================================================================================



//==================================================================================================
displayText();

//====================================================================================================

setInterval(function()
 {

    displayText();
    cookies = cookies + cookiesPerSecond;
    lifetimeCookies = lifetimeCookies + cookiesPerSecond;

  }, 1000);

//====================================================================================================

$("#cookie").click(function()
    {

      displayText();
      cookies = cookies + cookiesPerClick;
      lifetimeClicks = lifetimeClicks + 1;


      //if(lifetimeClicks < 2)
  //    {
  //      alert("In order for you to save you data you must login to your Github and click the save")
  //    }



});

//====================================================================================================

$("#save").click(function()
   {
     $.post( "/save",
       { "cookies": cookies ,"cookiesPerClick": cookiesPerClick,"cookiesPerSecond": cookiesPerSecond, "cursorsOwned": cursorsOwned, "costOfCursors": costOfCursors, "grandmasOwned": grandmasOwned, "costOfGrandmas": costOfGrandmas, "lifetimeClicks": lifetimeClicks, "lifetimeCookies":lifetimeCookies}
     );
     alert("Your data has been updated and saved in the database")

   });

//====================================================================================================

$("#cursor").click(function()
  {
    if(cookies >= costOfCursors)
    {
      displayText();
      cookiesPerClick = cookiesPerClick + cursorWeight;
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


//====================================================================================================

$("#grandma").click(function()
{
  if(cookies >= costOfGrandmas)
  {
    displayText();
    cookiesPerSecond = cookiesPerSecond + grandmaWeight;
    cookies = cookies - costOfGrandmas;
    grandmasOwned = grandmasOwned + 1;
    costOfGrandmas = costOfGrandmas + costOfGrandmasMultiplier;
    costOfGrandmasMultiplier = costOfGrandmasMultiplier + 1;

  }
  else
  {
  alert("Insufficiant Cookies. You need " + (costOfGrandmas - cookies) + " more cookies to make that purchase");
  }

});


});

//====================================================================================================
