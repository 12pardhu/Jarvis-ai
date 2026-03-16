import React, { useMemo, useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export default function AuthGate({ children }) {
  const [authed, setAuthed] = useState(() => localStorage.getItem("jarvis_authed") === "true");
  const [pin, setPin] = useState("");
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("");

  const requireAuth = useMemo(() => localStorage.getItem("jarvis_require_auth") === "true", []);

  const setOk = () => {
    localStorage.setItem("jarvis_authed", "true");
    setAuthed(true);
    setStatus("");
  };

  const voiceLogin = async () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setStatus("Speech Recognition not supported. Use PIN login.");
      return;
    }

    setBusy(true);
    setStatus("Listening for your passphrase…");

    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    rec.onresult = async (e) => {
      const phrase = (e.results?.[0]?.[0]?.transcript || "").trim();
      try {
        await axios.post(`${API_BASE}/auth/voice`, { phrase });
        setOk();
      } catch {
        setStatus("Voice login failed. Try again or use PIN.");
      } finally {
        setBusy(false);
      }
    };

    rec.onerror = () => {
      setStatus("Voice recognition failed. Use PIN login.");
      setBusy(false);
    };

    try {
      rec.start();
    } catch {
      setStatus("Could not start voice recognition. Use PIN login.");
      setBusy(false);
    }
  };

  const pinLogin = async () => {
    if (!pin) return;
    setBusy(true);
    setStatus("Verifying PIN…");
    try {
      await axios.post(`${API_BASE}/auth/pin`, { pin });
      setOk();
    } catch {
      setStatus("Invalid PIN.");
    } finally {
      setBusy(false);
    }
  };

  // If auth is not required, don’t block demo.
  if (!requireAuth) return children;
  if (authed) return children;

  return (
    <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#020617", color: "white" }}>
      <div style={{ width: 420, maxWidth: "92vw", background: "#0b1220", padding: 24, borderRadius: 12, border: "1px solid #1e293b" }}>
        <h2 style={{ marginTop: 0 }}>Secure Access</h2>
        <p style={{ opacity: 0.85, marginTop: 6 }}>
          Login using your voice passphrase or PIN to continue.
        </p>

        <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
          <button onClick={voiceLogin} disabled={busy} style={{ flex: 1 }}>Voice Login</button>
          <button
            onClick={() => {
              localStorage.setItem("jarvis_require_auth", "false");
              setStatus("Auth gate disabled in browser (backend may still require token).");
            }}
            disabled={busy}
            style={{ background: "#334155" }}
          >
            Skip (UI)
          </button>
        </div>

        <div style={{ marginTop: 18 }}>
          <div style={{ fontSize: 13, opacity: 0.85, marginBottom: 8 }}>PIN fallback</div>
          <div style={{ display: "flex", gap: 10 }}>
            <input
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              placeholder="Enter PIN"
              type="password"
              style={{ flex: 1, padding: 12, borderRadius: 8, border: "1px solid #1e293b", background: "#020617", color: "white" }}
            />
            <button onClick={pinLogin} disabled={busy || !pin}>Login</button>
          </div>
        </div>

        {status && (
          <div style={{ marginTop: 14, fontSize: 13, opacity: 0.9 }}>
            {status}
          </div>
        )}

        <div style={{ marginTop: 16, fontSize: 12, opacity: 0.7 }}>
          To enable the gate: open DevTools and run: <code>localStorage.setItem("jarvis_require_auth","true")</code>
        </div>
      </div>
    </div>
  );
}

