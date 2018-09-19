function getTransition() {
  var data = null
  var req = new XMLHttpRequest();
  req.open("GET", "./api/transition", false);
  req.send(null);
  if(req.readyState == 4 && req.status == 200) {
      data = req.responseText;
  };
  return JSON.parse(data)
}

var ctx = document.getElementById("barChart");
var barChart = new Chart(ctx, getTransition());
