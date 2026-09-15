import { ArrowUpRight, BatteryCharging, Blocks, CircleCheck, Compass, Layers3, Menu, Smartphone, Sparkles, Wifi } from "lucide-react";
import { FormEvent, useState } from "react";
import ReactMarkdown from "react-markdown";
import type { ChatResponse, Message } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8004";
const prompts = [
  ["Architecture", "Choose between Expo, React Native CLI, and Flutter for my app"],
  ["Navigation", "Design a tab and stack navigation flow for a delivery app"],
  ["API integration", "Plan secure authentication and offline API sync"],
  ["Release", "Prepare an iOS and Android release checklist"],
];

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(value: string) {
    const message = value.trim();
    if (!message || isSending) return;
    setMessages((current) => [...current, { role: "user", content: message }]);
    setDraft("");
    setError("");
    setIsSending(true);
    try {
      const response = await fetch(`${API_URL}/api/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message }) });
      if (!response.ok) throw new Error("The assistant could not complete that request.");
      const data = (await response.json()) as ChatResponse;
      setMessages((current) => [...current, { role: "assistant", content: data.answer, taskType: data.task_type }]);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Something went wrong.");
    } finally {
      setIsSending(false);
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    void sendMessage(draft);
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Smartphone size={19} /></div><div><strong>FIELDNOTE</strong><span>mobile agent</span></div></div>
      <div className="side-rule" />
      <p className="side-label">Workspace</p>
      <button className="new-chat" type="button" onClick={() => setMessages([])}><Sparkles size={16} /> New project brief</button>
      <div className="side-card"><span className="status-dot" /> API connected <small>LOCAL MODE</small></div>
      <div className="side-bottom"><div className="side-label">Focus areas</div><div className="focus-list"><span><Compass size={14} /> Navigation</span><span><Blocks size={14} /> API & auth</span><span><BatteryCharging size={14} /> Performance</span><span><CircleCheck size={14} /> Release</span></div></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><button className="menu-button" type="button"><Menu size={20} /></button><div className="crumb"><span>FIELDNOTE</span><b>/</b> MOBILE BUILD ROOM</div><div className="platforms"><span><Wifi size={14} /> API online</span><span>RN / Expo / Flutter</span></div></header>
      <section className="conversation">
        {messages.length === 0 ? <div className="welcome"><div className="welcome-kicker"><span className="signal" /> MOBILE APPLICATION DEVELOPMENT AGENT</div><h1>Make the next<br /><i>move</i> deliberate.</h1><p>From the first screen to the store submission, turn a mobile idea into a buildable plan with clear architecture, resilient states, and platform-aware decisions.</p><div className="prompt-grid">{prompts.map(([label, prompt]) => <button key={label} type="button" onClick={() => void sendMessage(prompt)}><span>{label}</span><ArrowUpRight size={16} /></button>)}</div><div className="principles"><span><Layers3 size={15} /> Reusable by default</span><span><CircleCheck size={15} /> States included</span><span><Smartphone size={15} /> Platform aware</span></div></div> : <div className="messages">{messages.map((message, index) => <article className={`message ${message.role}`} key={`${message.role}-${index}`}><div className="message-label">{message.role === "user" ? "YOU" : `MOBILE AGENT${message.taskType ? ` / ${message.taskType.replace("_", " ")}` : ""}`}</div>{message.role === "assistant" ? <ReactMarkdown>{message.content}</ReactMarkdown> : <p>{message.content}</p>}</article>)}{isSending && <div className="loading"><span /><span /><span /> shaping a build plan</div>}{error && <div className="error">{error}</div>}</div>}
      </section>
      <form className="composer" onSubmit={submit}><textarea value={draft} onChange={(event) => setDraft(event.target.value)} placeholder="Describe the app, feature, or release problem..." rows={1} /><button type="submit" disabled={isSending || !draft.trim()} aria-label="Send message"><ArrowUpRight size={20} /></button><div className="composer-hint">Enter to send <span>·</span> Your API key stays server-side</div></form>
    </main>
  </div>;
}
