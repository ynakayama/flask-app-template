function getBreakdown() {
  var data = null
  var req = new XMLHttpRequest();
  req.open("GET", "./api/breakdown", false);
  req.send(null);
  if(req.readyState == 4 && req.status == 200) {
      data = req.responseText;
  };
  return JSON.parse(data)
}

var ctx = document.getElementById("pieChart");
var pieChart = new Chart(ctx, getBreakdown());
