import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;
    
    try {
      const res = await fetch('http://localhost:8000/api/pregunta-resuelta/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        
        
        body: JSON.stringify({ pregunta: input }),
      });
      
      
      const data = await res.json();
      console.log(data);
      setResponse(data);
    } catch (error) {
      console.error('Error al contactar el backend:', error);
      setResponse('Hubo un error al enviar tu pregunta.');
    }

    setInput('');
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem' }}>
      <h1>Chatbot IA</h1>


      {response && (
        <div style={{ margin: '20px', background: '#f0f0f0', padding: '1rem', borderRadius: '8px' }}>
          <strong>Respuesta del bot:</strong>
          <p>{response}</p>
        </div>
      )}
            <input
        type="text"
        placeholder="Escribe tu pregunta..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: '80%', padding: '10px' }}
      />
      <button onClick={handleSend} style={{ padding: '10px', marginLeft: '10px' }}>
        Enviar
      </button>
    </div>
  );
}

export default App;
