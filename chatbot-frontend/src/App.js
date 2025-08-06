import React, { useState, useRef, useEffect } from 'react';


function App() {
  const [input, setInput] = useState('');
  // const [response, setResponse] = useState('');
  const [message, setMessage] = useState([]);
  const [categoria, setCategoria] = useState(null);

  const messageEndRef = useRef(null)

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({behavior : 'smooth'})
  },[message])

  const categorias = [
    {id:"1", nombre:"Marcajes"},
    {id:"2", nombre:"Acceso de Cuenta"},
    {id:"3", nombre:"Reduccion Laboral"},
    {id:"4", nombre:"Cargue de Mallas"},
    {id:"5", nombre:"Movimiento de Personal"}
  ]
  const handleCategoriaClick = (id, nombre) => {
    setCategoria(id);
    console.log(id);
    // puedes agregar una lógica si quieres añadir un mensaje automático
    setMessage([...message, { text: `Seleccionaste categoría ${nombre}, Cuentame como te puedo ayudar`, isUser: false }]);
  };

  const recargar = () => {
    setCategoria(null)
    setMessage([])
  }


  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {text : input, isUser : true}
    setMessage(prev => [...prev, userMessage])

    setInput('');

    try {
      const res = await fetch('http://localhost:8000/api/pregunta-resuelta/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        
        
        body: JSON.stringify({ pregunta: input }),
      });
      
      
      const data = await res.json();
      const botMessage = {text: data, isUser: false}
      setMessage(prev => [...prev, botMessage])

    } catch (error) {
      console.error('Error al contactar el backend:', error);
      const errorMessage = {text:'Hubo un error al enviar la pregunta', isUser:false}
      setMessage(prev => [...prev, errorMessage])

    }

    
  };

  return (
    <main >
      <div className='contenedor'> 
              <div className='titulo'><h1>Chatbot WFM</h1></div>

      {categoria === null ? (
        <div>
          <h3>Selecciona la categoria de tu consulta:</h3>
          <ul>
            {categorias.map((cat) => (
              <li key={cat.id}>
                <button onClick={() => handleCategoriaClick(cat.id, cat.nombre)}>{cat.nombre}</button>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <>
        
          {message.length !== 0 ? (
           
            message.map((msg, index) => (
              <li
                key={index}
                 className='message'
              >
                <span className={`message ${msg.isUser ? 'user-owner' : 'bot-owner'}`}>{msg.isUser ? 'Tú' : 'Bot'}</span>
                <p className={`message ${msg.isUser ? 'user-text' : 'bot-text'}`}>{msg.text}</p>
                {/* {msg.isUser ? (
                    <button onClick={() => recargar()}>Volver al Menú</button>
                  ) : null} */}
              </li>
              

            ))
          ) : (
            <h3 style={{ background: '#335a21ff' }}>
              Cuéntame, ¿en qué te puedo ayudar?
            </h3>
          )}
          <div ref={messageEndRef} />
        </>
      )}
      </div >
        <div className='form' >
          <input
              type="text"
              placeholder="Escribe tu pregunta..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={categoria === null}
            />
            <button onClick={handleSend} disabled={categoria === null} className='send'>
              Enviar
            </button>
            <button onClick={() => recargar()}>Volver al Menú</button>

        </div>
    </main>
  );
}

export default App;
