const navBtn = document.getElementById("nav-btn")
const navBottom = document.getElementById("nav-bottom-mobile")
const productImage = document.querySelector(".main-image")


function myFunction() {
    navBtn.classList.toggle('clicked')
    console.log(navBottom)
    if (navBottom.style.display === "none") {
        navBottom.style.display = "auto";
    } else {
        navBottom.style.display = "none";
    }
}

function changePic(img) {
    productImage.src = img.src
}