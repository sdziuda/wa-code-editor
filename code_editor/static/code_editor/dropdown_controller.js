function drop() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function dropEdit() {
  document.getElementById("myDropdownEdit").classList.toggle("show");
}

function dropOpt() {
  document.getElementById("myDropdownOptions").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    let dropdowns = document.getElementsByClassName("dropdown-content");
    let i;
    for (i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}