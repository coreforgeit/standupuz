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

    if (array[i]['places'] == 0) {
        mobBtnTg.classList.add('disabled');
        mobBtnTg.addEventListener('click', function (event) {
            event.preventDefault();
        });
    }
}
affiche_mob_btn_tg('.card_mob_btn_tg', card)

function affiche_mob_btn_copy(selector, array) {
    let mobBtnCopy = document.querySelector(selector)
    mobBtnCopy.setAttribute('href', array['tg_link'])

    if (array[i]['places'] == 0) {
        mobBtnCopy.classList.add('disabled');
        mobBtnCopy.addEventListener('click', function (event) {
            event.preventDefault();
        });
    }

    if (array[i]['places'] == 1) {
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