import React, { useState, useEffect } from 'react';
import common from 'styles/common.module.css'


export default function Home() {
  const [text, setText] = useState('');
  const [displayedText, setDisplayedText] = useState('');
  const [loading, setLoading] = useState(true);

  // Делаем запрос к API для получения текста
  useEffect(() => {
    fetch('http://localhost:8000/fox/')
      .then(
        response => response.json()
    )
      .then(data => setText(data.text))
      .catch(err => {
        console.error('Ошибка при загрузке текста:', err);
        setText('Не удалось загрузить текст');
      })
      .finally(() => setLoading(false));
  }, []);

  // После получения текста запускаем эффект печати
  useEffect(() => {
    console.log('ffffffffffffffffffff')
    console.log(text)

    if (!loading && text) {
        // setDisplayedText('');           // <-- Сбрасываем
        let index = 0;
        const interval = setInterval(() => {
          setDisplayedText(prev => prev + text.charAt(index));
          index++;                      // <-- инкремент после печати
          if (index >= text.length) {
            clearInterval(interval);
          }
        }, 150);
        return () => clearInterval(interval);
      }
    }, [loading, text]);

  if (loading) {
    return (
      <div className={common.container}>
        <p>Загрузка...</p>
      </div>
    );
  }


  return (
        <div className={common.container}>
          <h1 className={common.title}>{displayedText}</h1>
        </div>
      );
}


// export default function Home() {
//   const text = "Привет мир!";
//   const [displayedText, setDisplayedText] = useState("");

//   useEffect(() => {
//     let index = 0;
//     const interval = setInterval(() => {
//       setDisplayedText((prev) => prev + text.charAt(index));
//       index++;
//       if (index >= text.length) {
//         clearInterval(interval);
//       }
//     }, 150);
//     return () => clearInterval(interval);
//   }, []);

//   return (
//     <div className={common.container}>
//       <h1 className={common.title}>{displayedText}</h1>
//     </div>
//   );
// }
