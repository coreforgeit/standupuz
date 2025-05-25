import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AffichePage from './pages/AffichePage';
import AboutPage from './pages/AboutPage';
import EventMobPage from './pages/EventMobPage';
// import css from './static/site';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* <Route path="/" element={<AffichePage />} /> */}
        <Route path="/" element={<Navigate to="/events" replace />} />
        <Route path="/events" element={<AffichePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/event_mob/:id" element={<EventMobPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
