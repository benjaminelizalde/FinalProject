var count = 0;
  $(document).ready(function() {
    $("#test").click(function(){
      count = count + 1;
      $("#count").text(count);
