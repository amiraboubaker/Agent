import { Activity, ChevronDown, Menu, ShieldCheck, Sparkles } from "lucide-react";
import { useChat } from "./hooks/useChat";
import { Composer } from "./components/Composer";
import { MessageBubble } from "./components/MessageBubble";
import { Sidebar } from "./components/Sidebar";
import "./styles.css";

const suggestions = ["Deploy my Docker Compose app to a VPS", "Diagnose this Nginx 502 error", "Create a GitHub Actions deployment pipeline", "Harden my Ubuntu server and configure TLS"];

export default function App() {
    const chat = useChat();
    return <div className="app-shell"><Sidebar conversations={chat.conversations} onNew={chat.startNewConversation} /><main className="workspace"><header className="topbar"><button className="mobile-menu icon-button" type="button"><Menu size={20} /></button><div><span className="eyebrow">WORKSPACE / ASSISTANT</span><h1>DevOps and Cloud Infrastructure Agent</h1></div><div className="topbar-right"><span className="live-indicator"><Activity size={15} /> API online</span><button className="profile-button" type="button">DO</button></div></header><section className="chat-area"><div className="chat-scroll"><div className="welcome"><div className="welcome-icon"><Sparkles size={22} /></div><p className="eyebrow">YOUR INFRASTRUCTURE PARTNER</p><h2>What are we deploying<br /><em>today?</em></h2><p className="welcome-copy">Deploy, automate, monitor, troubleshoot, and secure applications across servers, containers, clusters, and cloud infrastructure.</p><div className="suggestions">{suggestions.map((suggestion) => <button key={suggestion} onClick={() => chat.sendMessage(suggestion)} type="button">{suggestion}</button>)}</div></div>{chat.messages.map((message, index) => <MessageBubble key={`${message.role}-${index}`} message={message} />)}{chat.isSending && <div className="thinking"><span></span><span></span><span></span> DevOps Agent is thinking</div>}{chat.error && <div className="error-banner"><strong>Request failed</strong><span>{chat.error}</span></div>}</div><Composer onSend={chat.sendMessage} disabled={chat.isSending} /></section><footer className="workspace-footer"><span><ShieldCheck size={14} /> Credentials stay on the server</span><span>v1.0 · <ChevronDown size={13} /></span></footer></main></div>;
}
