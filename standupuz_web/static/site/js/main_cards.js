function createCards(selector, array) {
    for (let i = 0; i < array.length; i++) {
        let item = document.createElement('a')
        item.classList.add('item', 'waves-effect', 'waves-light', 'btn', 'modal-trigger')
        if (window.innerWidth <= 768) {
            item.setAttribute("href", `../event_mob/${array[i]['event_id']}`);
        } else {
            item.setAttribute("href", `#modal${i}`);
        }
        // item.setAttribute("href", `#modal${i}`)
        item.style.backgroundImage = `url(${array[i]['photo_path']})`

        //информация о наличии мест
        let places = document.createElement('div')
        places.classList.add('places')
        if (array[i]['places'] == 1) {
            places.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'
            places.textContent = `Места есть`
        } else {
            places.style.backgroundColor = 'rgba(128, 117, 117, 1)'
            places.textContent = `Мест нет`
        }
        item.appendChild(places)

        //информация о мероприятии
        let info = document.createElement('div')
        info.classList.add('info')
        info.style.backgroundColor = 'rgba(240, 219, 220, 0.95)'
        item.appendChild(info)

        //информация о дате (дочерний к мероприятию)
        let date_day = document.createElement('div')
        date_day.classList.add('date_day')
        info.appendChild(date_day)

        //дата
        let date = document.createElement('div')
        date.classList.add('date')
        date.innerHTML = array[i]['date_str']
        date_day.appendChild(date)

        //день
        let day = document.createElement('div')
        day.classList.add('day')
        day.innerHTML = array[i]['day_str']
        date_day.appendChild(day)

        //информация о времени и месте (дочерний к мероприятию)
        let time_place = document.createElement('div')
        time_place.classList.add('time_place')
        info.appendChild(time_place)

        //время
        let time = document.createElement('div')
        time.classList.add('date')
        time.innerHTML = array[i]['time_str']
        time_place.appendChild(time)

        //место
        let place = document.createElement('div')
        place.classList.add('day')
        place.innerHTML = array[i]['place']
        time_place.appendChild(place)

        //информация о стоимости
        let text_price = document.createElement('div')
        info.appendChild(text_price)

        //текст
        let text1 = document.createElement('div')
        text1.classList.add('day')
        text1.innerHTML = `От`
        text_price.appendChild(text1)

        //price
        let price = document.createElement('div')
        price.classList.add('date')
        price.innerHTML = array[i]['min_amount']
        text_price.appendChild(price)

        //текст
        let text2 = document.createElement('div')
        text2.classList.add('day')
        text2.innerHTML = `UZS`
        text_price.appendChild(text2)

        document.querySelector(selector).append(item)
    }
}
createCards('.cards_grid', cards)


function createModal(selector, array) {
    for (let i = 0; i < array.length; i++) {
        let mod = document.createElement('div')
        mod.setAttribute('id', `modal${i}`)
        mod.classList.add('modal')

        let mod_content = document.createElement('div')
        mod_content.classList.add('modal-content')
        mod.appendChild(mod_content)

        //кнопка "закрыть"
        let close_mod = document.createElement('img')
        close_mod.setAttribute('src', '../static/site/img/close_modal.svg')
        close_mod.classList.add('modal-close')
        mod_content.appendChild(close_mod)

        //контент_флекс
        let content = document.createElement('div')
        content.classList.add('content_flex')
        mod_content.appendChild(content)

        //контент_left
        let content_left = document.createElement('p')
        content_left.classList.add('content_left')
        content_left.innerHTML = array[i]['description']
        content.appendChild(content_left)

        //контент_right
        let content_right = document.createElement('img')
        content_right.setAttribute('src', `${array[i]['photo_path']}`)
        content_right.classList.add('mod_img')
        content.appendChild(content_right)

        // //кнопки_футер
        let btn_all = document.createElement('div')
        btn_all.classList.add('mod_footer')
        mod_content.appendChild(btn_all)

        // //кнопка_ссылка на tg
        let btn_tg = document.createElement('a')
        btn_tg.classList.add('btn_tg')
        btn_tg.setAttribute('href', `${array[i]['tg_link']}`)
        btn_tg.innerHTML = `Забронировать через Telegram`
        btn_all.appendChild(btn_tg)

        //событие актив-неактив
        if (array[i]['places'] == 0) {
            btn_tg.classList.add('disabled');
            btn_tg.style.backgroundColor = 'rgba(128, 117, 117, 1)';
            btn_tg.style.color = 'rgba(178, 168, 168, 1)';
            btn_tg.addEventListener('click', function (event) {
                event.preventDefault();
            });
        }
        else {
            btn_tg.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'
            // изменение фона при клике на кнопку
            // btn_tg.addEventListener('click', function () {
            //     btn_tg.style.backgroundColor = 'rgba(128, 52, 56, 1)';
            // });

            // изменение фона при наведении на кнопку
            btn_tg.addEventListener('mouseover', function () {
                btn_tg.style.background = 'rgba(128, 52, 56, 1)'; // Цвет при наведении
            });
            btn_tg.addEventListener('mouseout', function () {
                btn_tg.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'; // Возвращение исходного цвета
            });
        }

        //кнопка "копировать ссылку"
        let btn_copy = document.createElement('a')
        btn_copy.classList.add('btn_copy')
        btn_copy.setAttribute('href', `${array[i]['tg_link']}`)
        btn_copy.setAttribute('title', `Копировать ссылку`)

        if (array[i]['places'] == 0) {
            btn_copy.classList.add('disabled');
            btn_copy.style.backgroundColor = 'rgba(128, 117, 117, 1)';
            btn_copy.addEventListener('click', function (event) {
                event.preventDefault();
            });
        }
        else {
            btn_copy.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'
            const linkToCopy = `${array[i]['tg_link']}`
            btn_copy.addEventListener('mouseover', function () {
                btn_copy.style.background = 'rgba(128, 52, 56, 1)'; // Цвет при наведении
            });
            btn_copy.addEventListener('mouseout', function () {
                btn_copy.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'; // Возвращение исходного цвета
            });
            btn_copy.addEventListener('click', function (even) {
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

        btn_all.appendChild(btn_copy)

        let copy_img = document.createElement('img')
        if (array[i]['places'] == 0) {
            copy_img.setAttribute('src', '../static/site/img/btn_copy_notActive.svg')
        }
        else {
            copy_img.setAttribute('src', '../static/site/img/btn_copy.svg')
        }
        btn_copy.appendChild(copy_img)

        // if (array[i]['places'] == 1) {
        //     const linkToCopy = `${array[i]['tg_link']}`
        //     btn_copy.addEventListener('click', function (even) {
        //         even.preventDefault();
        //         navigator.clipboard.writeText(linkToCopy)
        //             // .then(() => {
        //             //   // alert('Link copied to clipboard!')
        //             // })
        //             .catch(err => {
        //                 console.error('Failed to copy link: ', err)
        //             })
        //     })
        // }

        document.querySelector(selector).append(mod)
    }
}
createModal('body', cards)
