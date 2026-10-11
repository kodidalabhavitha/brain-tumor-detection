var cnn_graphs = document.getElementById("cnn");
var hom = document.getElementById("home");
var password_page = document.getElementById("password_page");

var b1 = document.getElementById("b1");
var b2 = document.getElementById("b2");
var b3 = document.getElementById("b3");
var b4 = document.getElementById("b4");
var b5 = document.getElementById("b5");

function cnn() {
  cnn_graphs.style.display = "block";
  password_page.style.display = "none";
  hom.style.display = "none";
  b5.classList.add("bg-secondary");
  b1.classList.add("bg-secondary");
  b2.classList.remove("bg-secondary");
  b3.classList.add("bg-secondary");
  b4.classList.add("bg-secondary");
}

function home() {
  cnn_graphs.style.display = "none";
  password_page.style.display = "none";
  hom.style.display = "block";
  b5.classList.add("bg-secondary");
  b1.classList.remove("bg-secondary");
  b2.classList.add("bg-secondary");
  b3.classList.add("bg-secondary");
  b4.classList.add("bg-secondary");
}

function password() {
  cnn_graphs.style.display = "none";
  password_page.style.display = "block";
  hom.style.display = "none";
  b5.classList.remove("bg-secondary");
  b1.classList.add("bg-secondary");
  b2.classList.add("bg-secondary");
  b3.classList.add("bg-secondary");
  b4.classList.add("bg-secondary");
}
