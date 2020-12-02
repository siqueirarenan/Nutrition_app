// When the user clicks on the button, open the modal
function open_modal(id) {
    if (id != "all") {
        document.getElementById(id).style.display = "block"; }
}

// When the user clicks on <span> (x), close the modal
function close_modal(id) {
  document.getElementById(id).style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == document.getElementById("myModal")) {
    document.getElementById("myModal").style.display = "none";
  }
}

function accordion(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}

function favourite(di) {
    if (document.getElementById(di.concat("r")).value == 0) {
        document.getElementById(di.concat("r")).value = 1;
        document.getElementById(di.concat("h")).className = "fas fa-heart";
    } else {
        document.getElementById(di.concat("r")).value = 0;
        document.getElementById(di.concat("h")).className = "far fa-heart";
    }
}