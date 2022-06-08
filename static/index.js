const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");
// show side bar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})
// close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

// change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
})

// توابع فس شاگردان

function discountFunction() {
    var baqi = document.getElementById("baqi").value;
    var fee = document.getElementById("fee").value;
    var discount = document.getElementById("descount").value;

    var mySelect = document.getElementById("mySelect").value;

    var dic = (discount * fee) / 100;
    dic = fee - dic;
    document.getElementById("amount").innerHTML = "Amount Pay: " + (dic - baqi);
    document.getElementById("level_bel").innerHTML = mySelect;
}



function popupToggle() {
    const popup = document.getElementById('popup');
    popup.classList.toggle('actived')
}
function analyticsToggle() {
    const popupana = document.getElementById('popupana');
    popupana.classList.toggle('actived')
}

// $(document).ready(function() {

//     $("#print").click(function() {
//         print("#result");
//     });

// });

// ختم توابع فس شاگردان


// function popupToggle() {
//     const popup = document.getElementById('popup');
//     popup.classList.toggle('active')
// }