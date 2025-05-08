// src/pages/AboutPage.jsx
import React, { useState, useEffect } from 'react';
import M from 'materialize-css';
import { API_BASE_URL, API_PATHS } from '../api/config';

export default function AboutPage() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    // Инициализируем мобильное меню Materialize
    M.Sidenav.init(document.querySelectorAll('.sidenav'), {
      edge: 'left',
      draggable: true,
    });

    // Загружаем данные «О нас»
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

  if (!info) {
    return <div>Loading...</div>;
  }

  const phone = info.phone;

  return (
    <>
      {/* Mobile Sidenav */}
      <ul id="slide-out" className="sidenav">
        <li>
          <button className="sidenav-close" aria-label="Закрыть меню">
            <img src="/site/img/Vector.svg" alt="Закрыть" />
          </button>
        </li>
        <li><a href="/events" className="sidenav-close">Афиша</a></li>
        <li><a href="/about"  className="sidenav-close menu_activ">О проекте</a></li>
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
            <div className="header_menu">
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
            </div>
            <div className="header_right">
              <a href="#!" data-target="slide-out" className="sidenav-trigger">
                <img src="/site/img/Menu.svg" alt="Меню" />
              </a>
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
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* About Section */}
      <section className="about">
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
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}
