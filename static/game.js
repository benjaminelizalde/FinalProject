var cookies = 0;
var cookiesPerSecond = 0;
var cookiesPerClick = 1;


  $(document).ready(function() {
    cookies = cookies + cookiesPerSecond;
    $("#cookies").text(cookies);
    $("#cookiesPerSecond").text(cookiesPerSecond);
    $("#cookiesPerClick").text(cookiesPerClick);



//====================================================================================================
    $("#cookie").click(function()
    {

      $("#cookies").text(cookies);
      $("#cookiesPerSecond").text(cookiesPerSecond);
      $("#cookiesPerClick").text(cookiesPerClick);
      cookies = cookies + cookiesPerClick;


    });

//====================================================================================================

	 $("#save").click(function()
   {

        cookiesPerClick = cookiesPerClick + 1;
        $("#cookies").text(cookies);
        $("#cookiesPerSecond").text(cookiesPerSecond);
        $("#cookiesPerClick").text(cookiesPerClick);

  });
//====================================================================================================

  $("#cursor").click(function(){
    $("#cookies").text(cookies);
    $("#cookiesPerSecond").text(cookiesPerSecond);
    $("#cookiesPerClick").text(cookiesPerClick);
      cookiesPerSecond = cookiesPerSecond + 1;

  });


});
