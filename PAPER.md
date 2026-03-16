## Title
**JarvisX: A Low-Latency Multilingual Voice Assistant with Hybrid Command Routing, Context Memory, and Secure Access**

## Abstract
Modern voice assistants often suffer from high latency when routing every request through large language models (LLMs), limited multilingual robustness, and weak security controls when performing system-level automation. This work presents JarvisX, a browser-based voice assistant that combines (i) a hybrid command router for instant execution of deterministic system actions and LLM fallback for open-ended dialogue, (ii) session-aware conversational memory for context continuity, (iii) a multilingual pipeline supporting English, Hindi, and Telugu with language detection and optional local translation services, and (iv) secure access controls using voice-phrase verification with PIN fallback. The system is implemented using a React frontend (Web Speech API + noise-aware gating) and a FastAPI backend integrating a lightweight local LLM (Ollama). Experiments on a scripted benchmark of automation commands and conversational queries demonstrate reduced action latency (instant lane) and improved perceived responsiveness, while maintaining competitive response quality for dialogue. Results include end-to-end latency, routing accuracy for automation intents, multilingual performance metrics, and robustness under noisy conditions.

## Problem Statement
- Existing assistants often **delay system actions** because they wait for an LLM response even for deterministic commands (e.g., “open chrome”).
- Multilingual voice interaction is often **inconsistent** for regional languages, and noisy environments degrade recognition quality.
- Automation without authentication creates **security risks** in desktop environments.

## Proposed System (High-level)
- **Frontend (React)**: browser voice capture (Web Speech API), optional noise gating, chat UI, session tracking.
- **Backend (FastAPI)**: command router, automation executor (cross-platform), memory module, multilingual module, authentication endpoints, LLM client (Ollama).

## Architecture (describe in paper)
1. **Speech Input Module** (frontend)
   - Push-to-talk + optional Noisy Mode gating (energy threshold).
2. **Command Router** (backend)
   - Lane A: rule/regex intent match → immediate automation.
   - Lane B: LLM fallback → contextual dialogue.
3. **Memory Module**
   - Session memory: last \(N\) turns per session_id.
   - Lightweight persistence store for retrieval snippets.
4. **Multilingual Module**
   - Detect language (en/hi/te).
   - Translate-to-English for routing/LLM, translate-back for response (optional local translator).
5. **Security Module**
   - Voice phrase verification (bcrypt hash).
   - PIN fallback verification.
   - Optional API token protection for endpoints.

## Methodology
### Hybrid Routing
- Define a deterministic allowlist for automation intents (open apps, open folders, file search, power controls).
- Execute automation immediately and return structured response.
- Only call the LLM when no automation intent matches.

### Context Memory
- Maintain session-based conversation window (last \(N\) turns).
- Inject “conversation so far” into the LLM prompt.
- Store lightweight interaction snippets for retrieval support.

### Multilingual Interaction
- Detect script-based language for English/Hindi/Telugu.
- Optional translation service (LibreTranslate-compatible) to normalize into English for router/LLM and translate responses back.

### Noise Robustness (Application-level)
- Implement “Noisy Mode” gating using WebAudio RMS thresholding before starting recognition.
- Use confidence thresholding to request re-try when recognition is uncertain.

### Security
- Authenticate via voice phrase or PIN; store hashed secrets in environment variables.
- Support optional API token header to protect the backend API.

## Experimental Setup
### Hardware/OS
- Evaluate on macOS / Windows / Linux (at least 2 systems if possible).

### Datasets / Test Suite
- **Automation commands**: 50–100 utterances (English/Hindi/Telugu) covering:
  - open chrome, open pictures, open downloads, find <file>, lock/sleep (power commands optional).
- **Conversation set**: 30 prompts requiring context recall across turns.
- **Noise conditions**:
  - quiet room (baseline)
  - noisy room (fan / corridor) or injected noise playback during speech

### Metrics
- **Latency**
  - \(T_{action}\): time from “send” to automation result return (ms)
  - \(T_{first}\): time-to-first-response token / chunk (WS)
  - \(T_{total}\): total response time (s)
- **Routing accuracy**
  - % of automation utterances correctly routed to instant lane
- **ASR robustness**
  - success rate and user re-try rate (quiet vs noisy mode)
- **Multilingual performance**
  - task success rate per language
- **Security**
  - authentication success rate / false reject rate for phrase, PIN success rate

## Results (template tables)
### Table 1: Latency
| Mode | Avg \(T_{action}\) ms | P95 \(T_{action}\) ms | Avg \(T_{total}\) s |
|------|------------------------|------------------------|----------------------|
| Instant lane (automation) | TBD | TBD | TBD |
| LLM lane (chat) | N/A | N/A | TBD |

### Table 2: Routing Accuracy
| Language | Automation utterances | Correctly routed | Accuracy |
|----------|------------------------|------------------|----------|
| English | TBD | TBD | TBD |
| Hindi | TBD | TBD | TBD |
| Telugu | TBD | TBD | TBD |

### Table 3: Noise Robustness
| Condition | Noisy Mode | Success rate | Re-try rate |
|-----------|------------|--------------|-------------|
| Quiet | Off | TBD | TBD |
| Noisy | Off | TBD | TBD |
| Noisy | On | TBD | TBD |

## Comparison with Traditional Assistants
Discuss:
- LLM-only pipeline vs hybrid router (latency + reliability)
- Typical assistants’ security posture vs explicit auth gating for automation
- Multilingual consistency for regional languages

## Conclusion
JarvisX demonstrates that hybrid command routing can significantly reduce latency for system actions while maintaining high-quality conversational capability via a lightweight local LLM. Session-based memory improves contextual continuity, and the application-level noise gating improves usability in non-ideal acoustic environments.

## Future Work
- Fully offline multilingual ASR (e.g., Whisper-based optional pipeline)
- Tool sandboxing + role-based permissions for sensitive automation
- Personalized memory with vector embeddings using a Python 3.13 compatible stack

