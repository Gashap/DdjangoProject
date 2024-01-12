let articleSections  = document.querySelectorAll('.description-short');


for (let articleSection of articleSections) {
    let moreButton = articleSection.querySelector('.more-button');
    let moreText = articleSection.querySelector('.description');
    moreButton.onclick = function () {
        if (moreText.style.height === "110px") {
            moreText.style.height = "auto";
            moreButton.innerHTML = "Скрыть";
        } else {
            moreText.style.height = "110px";
            moreButton.innerHTML = "Раскрыть";
        }
    }
}