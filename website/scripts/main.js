let period = document.getElementById("period");
let profile = document.getElementById("profile");
let profileItems = profile.getElementsByTagName("p");
let profileTexts = [];
let profileButton = document.getElementById("profile-button")

// Default show the first option
let index = period.selectedIndex;

for (let i = 0; i < profileItems.length; i++) {
    profileItems[i].style.display = "none";
}
profileItems[index].style.display = "inline";

// Change displayed innerText if option of period change
period.onchange = function() {
    index = this.selectedIndex
    for (let i = 0; i < profileItems.length; i++) {
        profileItems[i].style.display = "none";
    }
    profileItems[index].style.display = "inline";
}

// Choose to show the profile texts or not
profileButton.onclick = function() {
    if (profileItems[index].style.display == "none") {
        profileItems[index].style.display = "inline";
    } else {
        profileItems[index].style.display = "none";
    }
}