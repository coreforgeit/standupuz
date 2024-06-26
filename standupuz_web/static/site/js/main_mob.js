//html - event_mob
function affiche_mob_img(selector, array) {
    // for (let i = 0; i < array.length; i++) {
    let afficheMobImg = document.createElement('img')
    // afficheMobImg.setAttribute('src', `${array['photo_path']})`)
    afficheMobImg.setAttribute('src', array['photo_path'])
    afficheMobImg.classList.add('mod_img')

    document.querySelector(selector).append(afficheMobImg)
    // }
}
affiche_mob_img('.card_mob_img', card)

function affiche_mob_p(selector, array) {
    let afficheMobP = document.querySelector(selector)
    afficheMobP.innerHTML = `${array['description']}`
}
affiche_mob_p('.card_mob_p', card)

function affiche_mob_btn_tg(selector, array) {
    let mobBtnTg = document.querySelector(selector)
    mobBtnTg.setAttribute('href', `${array['tg_link']}`)

    if (array["places"] == 0) {
        mobBtnTg.style.backgroundColor = 'rgba(128, 117, 117, 1)';
        mobBtnTg.style.color = 'rgba(178, 167, 168, 1)';
        mobBtnTg.classList.add('disabled');
        mobBtnTg.addEventListener('click', function (event) {
            event.preventDefault();
        });
    } else {
        mobBtnTg.style.backgroundColor = 'rgba(247, 225, 226, 1)';
        mobBtnTg.style.color = 'rgba(128, 52, 56, 1)';
    }
}
affiche_mob_btn_tg('.card_mob_btn_tg', card)

function affiche_mob_btn_copy(selector, array) {
    let mobBtnCopy = document.querySelector(selector)
    mobBtnCopy.setAttribute('href', array['tg_link'])

    if (array['places'] == 0) {
        mobBtnCopy.classList.add('disabled');
        mobBtnCopy.addEventListener('click', function (event) {
            event.preventDefault();
        });
    }
    else {
        const linkToCopy = `${array['tg_link']}`
        mobBtnCopy.addEventListener('click', function (even) {
            even.preventDefault();
            navigator.clipboard.writeText(linkToCopy)
                // .then(() => {
                //   // alert('Link copied to clipboard!')
                // })
                .catch(err => {
                    console.error('Failed to copy link: ', err)
                })
        })
    }

}
affiche_mob_btn_tg('.card_mob_btn_copy', card)

function img_copy_link (selector, array) {
    let copyLink = document.querySelector(selector)
    let copyNot = "{% static 'site/img/btn_mob_copy_notActive.svg' %}"
    if(array['places'] == 0) {
        copyLink.setAttribute('src', copyNot)
    }
}
img_copy_link('.card_mob_btn_copy img', card)
