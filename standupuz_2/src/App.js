import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AffichePage from './pages/AffichePage';
import AboutPage from './pages/AboutPage';
import EventMobPage from './pages/EventMobPage';
// import css from './static/site';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AffichePage />} />
        <Route path="/events" element={<AffichePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/event_mob/:id" element={<EventMobPage />} />
        {/* <Route path="/about" element={<AboutPage />} /> */}
        {/* <Route path="/" element={<HomePage />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
