import { useState, useEffect, useRef } from 'react';

function App() {
  const [mensaje, setMensaje] = useState('');
  const [chat, setChat] = useState([]);
  const [cargando, setCargando] = useState(false);
  const chatEndRef = useRef(null); // Referencia para el auto-scroll

  // Función para hacer scroll automático al último mensaje
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat, cargando]);

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    const nuevoChat = [...chat, { rol: 'usuario', texto: mensaje }];
    setChat(nuevoChat);
    setMensaje('');
    setCargando(true);

   try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: mensaje }),
      });

      const data = await response.json();
      
      // Si el backend devuelve un error (Status 500, etc.), lo lanzamos al catch
      if (!response.ok) {
        throw new Error(data.detail || "Error desconocido en el servidor");
      }

      // Si todo sale bien, agregamos la respuesta de Gemma
      setChat([...nuevoChat, { rol: 'agente', texto: data.respuesta }]);
      
    } catch (error) {
      console.error("Error detectado:", error);
      // Ahora sí imprimirá el motivo real del fallo en la burbuja del agente
      setChat([...nuevoChat, { rol: 'agente', texto: `⚠️ Fallo: ${error.message}` }]);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col h-[85vh]">
        
        {/* Header */}
        <div className="bg-blue-800 text-white p-5 flex items-center justify-between shadow-md z-10">
          <div>
            <h1 className="text-xl font-bold">Memoria y Cuenta UNEG</h1>
            <p className="text-blue-200 text-sm">Asistente Administrativo Virtual</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span className="text-xs font-medium">En línea</span>
          </div>
        </div>

        {/* Área de Mensajes */}
        <div className="flex-1 overflow-y-auto p-5 bg-slate-50 space-y-6 no-scrollbar">
          {chat.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-3 opacity-70">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <p className="text-lg">Consulta los activos de la universidad</p>
            </div>
          ) : (
            chat.map((msg, index) => (
              <div key={index} className={`flex ${msg.rol === 'usuario' ? 'justify-end' : 'justify-start'} transition-all duration-300 ease-in-out`}>
                <div className={`max-w-[75%] px-5 py-3 rounded-2xl shadow-sm text-sm leading-relaxed ${
                  msg.rol === 'usuario' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-white text-slate-800 border border-slate-100 rounded-bl-none'
                }`}>
                  {msg.texto}
                </div>
              </div>
            ))
          )}

          {/* Indicador de "Escribiendo..." */}
          {cargando && (
            <div className="flex justify-start">
              <div className="bg-white border border-slate-100 text-slate-800 px-5 py-4 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-1">
                <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} /> {/* Punto de anclaje para el scroll automático */}
        </div>

        {/* Input de Texto */}
        <div className="p-4 bg-white border-t border-slate-100">
          <form onSubmit={enviarMensaje} className="flex gap-3">
            <input 
              type="text" 
              value={mensaje}
              onChange={(e) => setMensaje(e.target.value)}
              placeholder="Ej: ¿Cuántos pupitres hay en Puerto Ordaz?"
              className="flex-1 bg-slate-100 text-slate-800 px-5 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all border border-transparent focus:border-blue-300"
              disabled={cargando}
            />
            <button 
              type="submit" 
              disabled={cargando || !mensaje.trim()} 
              className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;