import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import gsap from "gsap";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";
import "./ChatWindow.css";

export default function ChatWindow() {

  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => localStorage.getItem("jarvis_session_id") || "");
  const [noisyMode, setNoisyMode] = useState(() => localStorage.getItem("jarvis_noisy_mode") === "true");

  const containerRef = useRef();

  useEffect(() => {
    gsap.from(".sidebar", {
      x: -200,
      opacity: 0,
      duration: 1
    });

    gsap.from(".chat-area", {
      opacity: 0,
      duration: 1.2
    });
  }, []);

  // 🔊 Text to Speech
  const speak = (text) => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  };

  const postToJarvis = async (text) => {
    const apiToken = localStorage.getItem("jarvis_api_token") || "";
    const res = await axios.post(
      "http://127.0.0.1:8000/jarvis-chat",
      { message: text, session_id: sessionId || undefined },
      apiToken ? { headers: { "X-API-Token": apiToken } } : undefined
    );

    const newSessionId = res.data.session_id;
    if (newSessionId && newSessionId !== sessionId) {
      setSessionId(newSessionId);
      localStorage.setItem("jarvis_session_id", newSessionId);
    }

    return res.data.response;
  };

  const resetSession = () => {
    localStorage.removeItem("jarvis_session_id");
    setSessionId("");
    setChat([]);
  };

  const waitForSpeech = async ({ threshold = 0.03, timeoutMs = 4000 } = {}) => {
    // Best-effort noise gating: wait until mic energy crosses threshold.
    // If anything fails, we simply proceed to start recognition immediately.
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 2048;
      source.connect(analyser);

      const buf = new Float32Array(analyser.fftSize);
      const start = performance.now();

      return await new Promise((resolve) => {
        const tick = () => {
          analyser.getFloatTimeDomainData(buf);
          let sum = 0;
          for (let i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
          const rms = Math.sqrt(sum / buf.length);
          const elapsed = performance.now() - start;

          if (rms >= threshold || elapsed >= timeoutMs) {
            try { stream.getTracks().forEach(t => t.stop()); } catch {}
            try { ctx.close(); } catch {}
            resolve(true);
            return;
          }
          requestAnimationFrame(tick);
        };
        tick();
      });
    } catch {
      return true;
    }
  };

  // 🎤 Voice Input (FINAL FIXED)
  const handleVoice = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setChat(prev => [
        ...prev,
        { role: "assistant", text: "⚠️ Speech Recognition not supported" }
      ]);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.maxAlternatives = 3;

    // 🎤 Listening UI
    setChat(prev => [
      ...prev,
      { role: "assistant", text: "🎤 Listening..." }
    ]);

    (async () => {
      if (noisyMode) {
        await waitForSpeech({ threshold: 0.035, timeoutMs: 5000 });
      }
      recognition.start();
    })();

    recognition.onresult = async (event) => {
      // Use the latest result and best alternative.
      const res = event.results[event.results.length - 1];
      if (!res || !res.isFinal) return;
      const best = Array.from(res).sort((a, b) => (b.confidence || 0) - (a.confidence || 0))[0];
      const text = (best?.transcript || "").trim();
      const confidence = best?.confidence ?? 0;

      if (!text) return;
      if (confidence && confidence < 0.6) {
        setChat(prev => [
          ...prev,
          { role: "assistant", text: "⚠️ I couldn't hear clearly. Please try again (or enable Noisy Mode)." }
        ]);
        return;
      }

      // 👤 User message
      setChat(prev => [
        ...prev,
        { role: "user", text }
      ]);

      // 🤖 Processing UI
      setChat(prev => [
        ...prev,
        { role: "assistant", text: "🤖 Processing..." }
      ]);

      try {
        const reply = await postToJarvis(text);

        setChat(prev => [
          ...prev,
          { role: "assistant", text: reply }
        ]);

        speak(reply);

      } catch (err) {
        setChat(prev => [
          ...prev,
          { role: "assistant", text: "⚠️ Error connecting to Jarvis." }
        ]);
      }
    };

    recognition.onerror = () => {
      setChat(prev => [
        ...prev,
        { role: "assistant", text: "⚠️ Voice recognition failed" }
      ]);
    };
  };

  // 💬 Send Text Message
  const send = async () => {

    if (!msg) return;

    const userMessage = msg;

    setChat(prev => [
      ...prev,
      { role: "user", text: userMessage }
    ]);

    setMsg("");
    setLoading(true);

    try {
      const reply = await postToJarvis(userMessage);

      setLoading(false);

      setChat(prev => [
        ...prev,
        { role: "assistant", text: reply }
      ]);

      speak(reply);

      setTimeout(() => {
        gsap.from(".bubble:last-child", {
          y: 20,
          opacity: 0,
          duration: 0.5
        });
      }, 100);

    } catch (error) {
      setLoading(false);

      setChat(prev => [
        ...prev,
        { role: "assistant", text: "⚠️ Error connecting to Jarvis." }
      ]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      send();
    }
  };

  return (
    <div className="app" ref={containerRef}>

      <div className="sidebar">
        <h2>🤖 Jarvis</h2>
        <p>AI Assistant</p>
      </div>

      <div className="chat-area">

        <div className="chat-container">

          {chat.map((c, i) => (
            <div key={i} className={c.role === "user" ? "user-row" : "ai-row"}>
              <div className="bubble">
                <ReactMarkdown
                  components={{
                    code({ inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline && match ? (
                        <SyntaxHighlighter
                          style={tomorrow}
                          language={match[1]}
                          PreTag="div"
                          {...props}
                        >
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      ) : (
                        <code {...props}>{children}</code>
                      );
                    }
                  }}
                >
                  {c.text}
                </ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && (
            <div className="ai-row">
              <div className="bubble typing">
                🤖 Jarvis is typing...
              </div>
            </div>
          )}

        </div>

        <div className="input-area">

          <input
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask Jarvis anything..."
          />

          <button onClick={send}>Send</button>
          <button onClick={handleVoice}>🎤</button>
          <button onClick={resetSession}>Reset Memory</button>
          <label style={{ marginLeft: 12, color: "white", display: "flex", alignItems: "center", gap: 6 }}>
            <input
              type="checkbox"
              checked={noisyMode}
              onChange={(e) => {
                const v = e.target.checked;
                setNoisyMode(v);
                localStorage.setItem("jarvis_noisy_mode", String(v));
              }}
            />
            Noisy Mode
          </label>

        </div>

      </div>

    </div>
  );
}