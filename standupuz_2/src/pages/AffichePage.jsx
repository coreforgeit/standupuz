// src/pages/AffichePage.jsx
import React, { useState, useEffect } from 'react'
import M from 'materialize-css'
import { API_BASE_URL, API_PATHS } from '../api/config'
import { Helmet } from 'react-helmet'
// import { fetchInfo } from '../utils/base'

export default function AffichePage() {
  const [cards, setCards] = useState([])
  const [phone, setPhone] = useState('')

  // инициализация Sidenav, загрузка events и info
  useEffect(() => {
    M.Sidenav.init(document.querySelectorAll('.sidenav'), {
      edge: 'right',
      draggable: true,
    })

    async function fetchEvents() {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.events}`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        setCards(data.cards || [])
      } catch (err) {
        console.error('Error loading events:', err)
      }
    }

    async function fetchInfo() {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.info}`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const { phone } = await res.json()
        setPhone(phone)
      } catch (err) {
        console.error('Error loading info:', err)
      }
    }

    fetchEvents()
    fetchInfo()
  }, [])

  // инициализация модалей после загрузки карточек
  useEffect(() => {
    if (cards.length) {
      M.Modal.init(document.querySelectorAll('.modal'))
    }
  }, [cards])

  const isMobile = window.innerWidth <= 768

  return (
    <>

    <Helmet>
      <title>StandUp - Афиша</title>
      <meta name="description" content="Расписание ближайших стендап-шоу в Ташкенте от StandUpUz" />
      <link rel="canonical" href="https://standupcomedy.uz/events" />
      <meta property="og:title" content="Афиша StandUpUz" />
      <meta property="og:description" content="Расписание ближайших стендап-шоу в Ташкенте от StandUpUz" />
      <meta property="og:url" content="https://standupcomedy.uz/events" />
      <meta property="og:type" content="website" />

       <script type="application/ld+json">{`
        {
          "@context": "https://schema.org",
          "@type": "ItemList",
          "itemListElement": [
            ${cards.map((card, idx) => `{
              "@type": "Event",
              "position": ${idx + 1},
              "name": "${card.title}",
              "startDate": "${card.date_str}T${card.time_str}:00",
              "url": "https://standupcomedy.uz/event/${card.event_id}"
            }`).join(',')}
          ]
        }
        `}</script>

    </Helmet>


      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="header_flex">
            <div className="header_logo">
              <img
                className="logo"
                src="/site/img/WhiteSUz_wof_Png 2.svg"
                alt="StandUpUz"
              />
            </div>
            <div className="header_menu">
              <ul className="header_menu_ul">
                <li><a className="menu_activ" href="/events">Афиша</a></li>
                <li><a className="menu_notActiv" href="/about">О проекте</a></li>
              </ul>
            </div>
            <div className="header_right">
              <div className="header_right_burger">
                <a href="#!" data-target="slide-out" className="sidenav-trigger">
                  <img src="/site/img/Menu.svg" alt="Меню" />
                </a>
              </div>
              <div className="header_right_phone phone">
                <a href={`tel:${phone}`}>{phone}</a>
              </div>
              <div className="header_right_contacts">
                <a
                  href="https://instagram.com/standup.uz"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/Instagram.svg" alt="Instagram" />
                </a>
                <a
                  href="https://t.me/StandUp_UZB"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/Telegram.svg" alt="Telegram" />
                </a>
                <a
                  href="https://t.me/standup_uztg"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/Telegram.svg" alt="Telegram" />
                </a>
                <a
                  href="https://www.youtube.com/channel/UCtDA0xLMJ76jg0vmdk7FZdw"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/youtube.png" alt="YouTube" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidenav */}
      <ul id="slide-out" className="sidenav">
        <li>
          <button className="sidenav-close" aria-label="Закрыть меню">
            <img src="/site/img/Vector.svg" alt="Закрыть" />
          </button>
        </li>
        <li><a href="/events" className="sidenav-close">Афиша</a></li>
        <li><a href="/about" className="sidenav-close">О проекте</a></li>
      </ul>

      {/* Cards Section */}
      <section className="cards">
        {/* <h1>Афиша StandUpUz</h1> */}
        <div className="container">
          <div className="cards_grid">
            {cards.map((card, idx) => {
              const imgPath = card.photo_path.replace(/^\.\.\//, '')
              const imageUrl = `${API_BASE_URL}/${imgPath}`
              const href = isMobile
                ? `/event_mob/${card.event_id}`
                : `#modal${idx}`
              const modalClass = isMobile ? '' : 'modal-trigger'
              const hasPlaces = card.places > 0

              return (
                <a
                  key={card.event_id}
                  href={href}
                  className={`item waves-effect waves-light btn ${modalClass}`}
                  style={{ backgroundImage: `url(${imageUrl})` }}
                >
                  <div
                    className="places"
                    style={hasPlaces
                      ? { background: 'linear-gradient(180deg, #993F43 0%, #803438 100%)' }
                      : { backgroundColor: 'rgba(128, 117, 117, 1)' }}
                  >
                    {hasPlaces ? 'Места есть' : 'Мест нет'}
                  </div>
                  <div className="info" style={{ backgroundColor: 'rgba(240,219,220,0.95)' }}>
                    <div className="date_day">
                      <div className="date">{card.date_str}</div>
                      <div className="day">{card.day_str}</div>
                    </div>
                    <div className="time_place">
                      <div className="date">{card.time_str}</div>
                      <div className="day">{card.place}</div>
                    </div>
                    <div className="text_price">
                      <div className="day">От</div>
                      <div className="date">{card.min_amount}</div>
                      <div className="day">UZS</div>
                    </div>
                  </div>
                </a>
              )
            })}
          </div>
        </div>
      </section>

      {/* Modals */}
      {cards.map((card, idx) => {
        const imgPath = card.photo_path.replace(/^\.\.\//, '')
        const imageUrl = `${API_BASE_URL}/${imgPath}`
        const hasPlaces = card.places > 0

        return (
          <div id={`modal${idx}`} className="modal" key={`modal${idx}`}>
            <div className="modal-content">
              <img
                src="/site/img/close_modal.svg"
                className="modal-close"
                alt="Закрыть"
              />
              <div className="content_flex">
                <p
                  className="content_left"
                  dangerouslySetInnerHTML={{ __html: card.description }}
                />
                <img src={imageUrl} className="mod_img" alt={card.place} />
              </div>
              <div className="mod_footer">
                <a
                  href={card.tg_link}
                  className={`btn_tg ${!hasPlaces ? 'disabled' : ''}`}
                  style={
                    hasPlaces
                      ? { background: 'linear-gradient(180deg, #993F43 0%, #803438 100%)' }
                      : { backgroundColor: 'rgba(128,117,117,1)', color: 'rgba(178,168,168,1)' }
                  }
                  onClick={e => !hasPlaces && e.preventDefault()}
                  onMouseOver={e => {
                    e.currentTarget.style.background = 'rgba(128, 52, 56, 1)';
                  }}
                  onMouseOut={e => {
                    e.currentTarget.style.background = hasPlaces
                      ? 'linear-gradient(180deg, #993F43 0%, #803438 100%)'
                      : 'rgba(128,117,117,1)';
                  }}
                >
                  Забронировать через Telegram
                </a>
                <a
                  href="#"
                  className={`btn_copy ${!hasPlaces ? 'disabled' : ''}`}
                  title="Копировать ссылку"
                  style={
                    hasPlaces
                      ? { background: 'linear-gradient(180deg, #993F43 0%, #803438 100%)' }
                      : { backgroundColor: 'rgba(128,117,117,1)' }
                  }
                  onClick={e => {
                    e.preventDefault()
                    if (hasPlaces) {
                      navigator.clipboard.writeText(card.tg_link).catch(err => console.error('Copy failed:', err))
                    }
                  }}
                  onMouseOver={e => {
                    if (hasPlaces) e.currentTarget.style.background = 'rgba(128, 52, 56, 1)'
                  }}
                  onMouseOut={e => {
                    if (hasPlaces) e.currentTarget.style.background = 'linear-gradient(180deg, #993F43 0%, #803438 100%)'
                  }}
                >
                  <img
                    src={
                      hasPlaces
                        ? '/site/img/btn_copy.svg'
                        : '/site/img/btn_copy_notActive.svg'
                    }
                    alt="Копировать"
                  />
                </a>
              </div>
            </div>
          </div>
        )
      })}

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer_flex">
            <div className="phone">
              <a href={`tel:${phone}`}>{phone}</a>
            </div>
            <div className="header_right_contacts">
              <a
                href="https://instagram.com/standup.uz"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img src="/site/img/Instagram.svg" alt="Instagram" />
              </a>
              <a
                href="https://t.me/StandUp_UZB"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img src="/site/img/Telegram.svg" alt="Telegram" />
              </a>
              <a
                  href="https://t.me/standup_uztg"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/Telegram.svg" alt="Telegram" />
                </a>
                <a
                  href="https://www.youtube.com/channel/UCtDA0xLMJ76jg0vmdk7FZdw"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img src="/site/img/youtube.png" alt="YouTube" />
                </a>
            </div>
          </div>
        </div>
      </footer>
    </>
  )
}
