
var count = 0;
  $(document).ready(function() {
    $("#cookie").click(function(){
      count = count + 1;
      $("#count").text(count);
    });
});

$("#save").click(function(){
  $.post("/save",count);
  alert("hi");
})
