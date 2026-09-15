import { Activity, ChevronDown, Menu, ShieldCheck, Sparkles } from "lucide-react";
import { useChat } from "./hooks/useChat";
import { Composer } from "./components/Composer";
import { MessageBubble } from "./components/MessageBubble";
import { Sidebar } from "./components/Sidebar";
import "./styles.css";

const suggestions = ["Help me define the problem and target users", "Shape a focused MVP for this idea", "Prioritize features by user value", "Design experiments for my riskiest assumptions"];

export default function App() {
    const chat = useChat();
    return <div className="app-shell"><Sidebar conversations={chat.conversations} onNew={chat.startNewConversation} /><main className="workspace"><header className="topbar"><button className="mobile-menu icon-button" type="button"><Menu size={20} /></button><div><span className="eyebrow">WORKSPACE / ASSISTANT</span><h1>Product Management Agent</h1></div><div className="topbar-right"><span className="live-indicator"><Activity size={15} /> API online</span><button className="profile-button" type="button">PM</button></div></header><section className="chat-area"><div className="chat-scroll"><div className="welcome"><div className="welcome-icon"><Sparkles size={22} /></div><p className="eyebrow">YOUR PRODUCT PARTNER</p><h2>What are we building<br /><em>today?</em></h2><p className="welcome-copy">Turn a problem into a focused product plan with clear users, a small MVP, measurable outcomes, and experiments that reduce uncertainty.</p><div className="suggestions">{suggestions.map((suggestion) => <button key={suggestion} onClick={() => chat.sendMessage(suggestion)} type="button">{suggestion}</button>)}</div></div>{chat.messages.map((message, index) => <MessageBubble key={`${message.role}-${index}`} message={message} />)}{chat.isSending && <div className="thinking"><span></span><span></span><span></span> Product Management Agent is thinking</div>}{chat.error && <div className="error-banner"><strong>Request failed</strong><span>{chat.error}</span></div>}</div><Composer onSend={chat.sendMessage} disabled={chat.isSending} /></section><footer className="workspace-footer"><span><ShieldCheck size={14} /> Your API key stays on the server</span><span>v1.0 · <ChevronDown size={13} /></span></footer></main></div>;
}
