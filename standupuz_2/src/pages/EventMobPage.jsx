// src/pages/EventMobPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import M from 'materialize-css';
import { API_BASE_URL, API_PATHS } from '../api/config';
import { Helmet } from 'react-helmet';

export default function EventMobPage() {
  const { id } = useParams();
  const [card, setCard] = useState(null);
  const [phone, setPhone] = useState('');

  useEffect(() => {
    // инициализируем боковое меню Materialize
    M.Sidenav.init(document.querySelectorAll('.sidenav'), {
      edge: 'left',
      draggable: true,
    });

    // загружаем детали события
    const fetchCard = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.events}${id}/`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        // API отдаёт { cards: [...] } для списка, но для одиночного события — просто объект
        setCard(data.card || data);
      } catch (err) {
        console.error('Error loading event:', err);
      }
    };

    // загружаем номер телефона из info
    const fetchInfo = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.info}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const { phone } = await res.json();
        setPhone(phone);
      } catch (err) {
        console.error('Error loading info:', err);
      }
    };

    fetchCard();
    fetchInfo();
  }, [id]);

  if (!card) {
    return <div>Загрузка...</div>;
  }

  // избавляемся от ведущих "../" в пути
  const imgPath = card.photo_path.replace(/^\.\.\//, '');
  const imageUrl = `${API_BASE_URL}/${imgPath}`;
  const hasPlaces = card.places > 0;
  const copyIcon = hasPlaces
    ? '/site/img/btn_mob_copy.svg'
    : '/site/img/btn_mob_copy_notActive.svg';
  // const tgBtnStyle = hasPlaces
  //   ? { backgroundColor: 'rgba(247, 225, 226, 1)', color: 'rgba(128, 52, 56, 1)' }
  //   : { backgroundColor: 'rgba(128, 117, 117, 1)', color: 'rgba(178, 167, 168, 1)' };
  const tgBtnStyle = (hasPlaces || card.ticket_url)
    ? { backgroundColor: 'rgba(247, 225, 226, 1)', color: 'rgba(128, 52, 56, 1)' }
    : { backgroundColor: 'rgba(128, 117, 117, 1)', color: 'rgba(178, 167, 168, 1)' };
  const tgBtnClass = hasPlaces ? '' : 'disabled';
  const btnLink = card.ticket_url ? card.ticket_url : card.tg_lin
  const btnTetx = card.ticket_url ? 'Забронировать места' : 'Забронировать через Telegram'

  return (
    <>
      <Helmet>
        <title>{card.title} | StandUpUz</title>
        <meta name="description" content={card.description.replace(/<[^>]>/g, '').slice(0, 155)} />
        <link rel="canonical" href={`https://standupcomedy.uz/event/${id}`} />

        {/* Open Graph */}
        <meta property="og:title" content={card.title} />
        <meta property="og:description" content={card.description.replace(/<[^>]>/g, '').slice(0, 155)} />
        <meta property="og:image" content={imageUrl} />
        <meta property="og:url" content={`https://standupcomedy.uz/event/${id}`} />
        <meta property="og:type" content="event" />

        {/* JSON-LD для события */}
        <script type="application/ldjson">{`
      {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": "${card.name}",
        "startDate": "${card.date_str}T${card.time_str}:00",
        "location": {
          "@type": "Place",
          "name": "${card.place}"
        },
        "image": "${imageUrl}",
        "description": "${card.description.replace(/<[^>]>/g, '')}"
      }
      `}</script>
      </Helmet>

      {/* Mobile sidenav */}
      <ul id="slide-out" className="sidenav">
        <li>
          <button className="sidenav-close" aria-label="Закрыть меню">
            <img src="/site/img/Vector.svg" alt="Закрыть" />
          </button>
        </li>
        <li><a href="/events" className="sidenav-close">Афиша</a></li>
        <li><a href="/about" className="sidenav-close">О проекте</a></li>
      </ul>

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
            <div className="header_right">
              <a href="#!" data-target="slide-out" className="sidenav-trigger">
                <img src="/site/img/Menu.svg" alt="Меню" />
              </a>
              <div className="header_right_phone phone">
                <a href={`tel:${phone}`}>{phone}</a>
              </div>
              <div className="header_right_contacts">
                <a href="https://instagram.com/standup.uz" target="_blank" rel="noopener noreferrer">
                  <img src="/site/img/Instagram.svg" alt="Instagram" />
                </a>
                <a href="https://t.me/StandUp_UZB" target="_blank" rel="noopener noreferrer">
                  <img src="/site/img/Telegram.svg" alt="Telegram" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile event card (по макету index_affiche_mob.html) :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1} */}
      <div className="cards_mob">
        <div className="container">
          {/* <h1>{card.title}</h1> */}
          <div className="card_mob_img">
            <img src={imageUrl} alt={card.place} className="card_mob_img__inner" />
          </div>
          <p
            className="card_mob_p"
            dangerouslySetInnerHTML={{ __html: card.description }}
          />
          <div className="card_mob_footer">
            {/* кнопка бронирования */}
            <a
              href={btnLink}
              className={`card_mob_btn_tg ${tgBtnClass}`}
              style={tgBtnStyle}
              onClick={e => { if (!hasPlaces) e.preventDefault(); }}
              target="_blank"
              rel="noopener noreferrer"
            >
              {btnTetx}
            </a>

            {/* кнопка копирования ссылки */}
            <a
              href={card.tg_link}
              className={`card_mob_btn_copy ${!hasPlaces ? 'disabled' : ''}`}
              title="Копировать ссылку"
              style={hasPlaces
                ? { backgroundColor: 'rgba(247, 225, 226, 1)' }
                : { backgroundColor: 'rgba(128, 117, 117, 1)' }
              }
              onClick={e => {
                e.preventDefault();
                if (hasPlaces) navigator.clipboard.writeText(card.tg_link).catch(console.error);
              }}
            >
              <img
                src={copyIcon}
                alt="Копировать"
              />
            </a>
          </div>
        </div>
      </div>
    </>
  );
}
