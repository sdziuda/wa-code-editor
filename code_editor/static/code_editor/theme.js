function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
    document.getElementById("theme-switch").checked = themeName === 'theme-dark';
}

function toggleTheme() {
   if (localStorage.getItem('theme') === 'theme-dark'){
       setTheme('theme-light');
   } else {
       setTheme('theme-dark');
   }
   change_tab(localStorage.getItem('tab'));
}

(function () {
    let theme = localStorage.getItem('theme');
    if (theme === null) {
        setTheme('theme-dark');
    } else {
        setTheme(theme);
    }
})();