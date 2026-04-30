import { useState, useEffect, useRef } from 'react';
import { Bot, Send, Loader } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { chatAPI } from '../services/api';

export default function Asistente() {
  const [mensaje, setMensaje] = useState('');
  const [chat, setChat] = useState([]);
  const [cargando, setCargando] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [chat, cargando]);

  const enviar = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;
    const nuevoChat = [...chat, { rol: 'usuario', texto: mensaje }];
    setChat(nuevoChat);
    setMensaje('');
    setCargando(true);
    try {
      // Pasamos el chat actual como historial (excluyendo el msj actual)
      const data = await chatAPI.consultar(mensaje, chat);
      setChat([...nuevoChat, { rol: 'agente', texto: data.respuesta }]);
    } catch (error) {
      setChat([...nuevoChat, { rol: 'agente', texto: `Error: ${error.message}` }]);
    } finally { setCargando(false); }
  };

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Asistente Virtual IA</h2>
          <p className="page__subtitle">Consulta el inventario en lenguaje natural (Llama 3.2:3B)</p>
        </div>
        <div className="status-badge"><span className="status-dot"></span> Modelo Local</div>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {chat.length === 0 ? (
            <div className="chat-empty">
              <Bot size={48} />
              <h3>Asistente de Inventario UNEG</h3>
              <p>Preguntame sobre bienes, sedes, cantidades o cualquier dato del inventario.</p>
              <div className="chat-suggestions">
                {['Cuantos bienes hay en total?', 'Que sedes tiene la UNEG?', 'Cuantas computadoras hay?'].map(s => (
                  <button key={s} className="chat-suggestion" onClick={() => setMensaje(s)}>{s}</button>
                ))}
              </div>
            </div>
          ) : chat.map((msg, i) => (
            <div key={i} className={`chat-bubble chat-bubble--${msg.rol}`}>
              <div className="chat-bubble__content markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.texto}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          {cargando && (
            <div className="chat-bubble chat-bubble--agente">
              <div className="chat-bubble__content chat-typing"><span></span><span></span><span></span></div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={enviar} className="chat-input">
          <input type="text" value={mensaje} onChange={e => setMensaje(e.target.value)} placeholder="Ej: Cuantos pupitres hay en Puerto Ordaz?" disabled={cargando} />
          <button type="submit" disabled={cargando || !mensaje.trim()}><Send size={18} /></button>
        </form>
      </div>
    </div>
  );
}
