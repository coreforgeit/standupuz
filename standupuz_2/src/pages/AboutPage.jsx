// src/pages/AboutPage.jsx
import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';

import M from 'materialize-css';
import { API_BASE_URL, API_PATHS } from '../api/config';

export default function AboutPage() {
  const [info, setInfo] = useState(null);

  // 1) Загружаем данные «О нас»
  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}${API_PATHS.info}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setInfo(data);
      } catch (err) {
        console.error('Error loading info:', err);
      }
    };
    fetchInfo();
  }, []);

  // 2) Инициализируем sidenav после того, как info подтянулось и меню отрисовалось
  useEffect(() => {
    if (info) {
      M.Sidenav.init(document.querySelectorAll('.sidenav'), {
        edge: 'right',
        draggable: true,
      });
    }
  }, [info]);

  if (!info) {
    return <div>Loading...</div>;
  }

  const phone = info.phone;

  return (
    <>
      <Helmet>
        <title>StandUp - О нас</title>
        <meta name="description" content={info.text.slice(0, 155)} />
        <link rel="canonical" href="https://standupcomedy.uz/about" />
        {/* Open Graph */}
        <meta property="og:title" content="StandUp - О нас" />
        <meta property="og:description" content={info.text.slice(0, 155)} />
        <meta property="og:url" content="https://standupcomedy.uz/about" />
        <meta property="og:type" content="website" />
        {/* JSON-LD для организации */}
        <script type="application/ldjson">{`
       {
         "@context": "https://schema.org",
         "@type": "Organization",
         "name": "StandUpUz",
         "url": "https://standupcomedy.uz",
         "logo": "https://standupcomedy.uz/site/img/WhiteSUz_wof_Png%202.svg"
       }
     `}</script>
      </Helmet>

      {/* Mobile Sidenav */}
      <ul id="slide-out" className="sidenav">
        <li>
          <button className="sidenav-close" aria-label="Закрыть меню">
            <img src="/site/img/Vector.svg" alt="Закрыть" />
          </button>
        </li>
        <li>
          <a href="/events" className="sidenav-close">
            Афиша
          </a>
        </li>
        <li>
          <a href="/about" className="sidenav-close menu_activ">
            О проекте
          </a>
        </li>
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
            <nav className="header_menu">
              <ul className="header_menu_ul">
                <li>
                  <a className="menu_notActiv" href="/events">
                    Афиша
                  </a>
                </li>
                <li>
                  <a className="menu_activ" href="/about">
                    О проекте
                  </a>
                </li>
              </ul>
            </nav>
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

      {/* About Section */}
      <section className="about">
        {/* <h1>О проекте StandUpUz</h1> */}
        <div className="container">
          <div
            className="about_text"
            dangerouslySetInnerHTML={{ __html: info.text }}
          />
        </div>
      </section>

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
  );
}
