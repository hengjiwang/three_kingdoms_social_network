let period = document.getElementById("period");
let article = document.getElementsByClassName("main-intro")[0];
period.onchange = function() {
    let mySelect = this[this.selectedIndex].value;
    if (mySelect == "all-periods") {
        article.innerHTML = "all-periods";
    } else if (mySelect == "yellow-turban-rebellion") {
        article.innerHTML = "yellow-turban-rebellion";
    } else if (mySelect == "dong-zhuo-in-power") {
        article.innerHTML = "dong-zhuo-in-power";
    } else if (mySelect == "rivalry-of-warlords") {
        article.innerHTML = "rivalry-of-warlords";
    } else if (mySelect == "battle-of-guandu") {
        article.innerHTML = "battle-of-guandu";
    } else if (mySelect == "battle-of-red-cliffs") {
        article.innerHTML = "battle-of-red-cliffs";
    } else if (mySelect == "liu-bei's-era") {
        article.innerHTML = "liu-bei's-era";
    } else if (mySelect == "northern-expeditions") {
        article.innerHTML = "northern-expeditions";
    } else {
        article.innerHTML = "post-zhuge-era";
    }
}