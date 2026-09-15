import { Cloud, Clock3, Plus } from "lucide-react";
import type { Conversation } from "../types";

export function Sidebar({ conversations, onNew }: { conversations: Conversation[]; onNew: () => void }) {
    return <aside className="sidebar">
        <div className="brand"><span className="brand-mark"><Cloud size={19} /></span><span>ops<span className="brand-dot">.</span></span></div>
        <button className="new-chat-button" onClick={onNew} type="button"><Plus size={17} /> New conversation</button>
        <div className="history-heading"><span>Recent incidents</span><Clock3 size={14} /></div>
        <div className="history-list">{conversations.length === 0 ? <p className="empty-history">Your sessions will appear here.</p> : conversations.map((conversation) => <div className="history-item" key={conversation.id}><span className={`history-icon ${conversation.task_type}`}></span><div><strong>{conversation.title}</strong><small>{conversation.task_type} · {conversation.message_count} messages</small></div></div>)}</div>
        <div className="sidebar-footer"><span className="status-dot"></span> Local workspace · SQLite</div>
    </aside>;
}
