import { useState } from "react";
import { Check, Copy, UserRound, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import type { Message } from "../types";

export function MessageBubble({ message }: { message: Message }) {
    const [copied, setCopied] = useState(false);
    const isUser = message.role === "user";

    async function copyMessage() {
        await navigator.clipboard.writeText(message.content);
        setCopied(true);
        window.setTimeout(() => setCopied(false), 1600);
    }

    return (
        <article className={`message-row ${isUser ? "message-row-user" : ""}`}>
            <div className={`avatar ${isUser ? "avatar-user" : "avatar-agent"}`}>{isUser ? <UserRound size={17} /> : <Sparkles size={17} />}</div>
            <div className="message-content">
                <div className="message-meta"><strong>{isUser ? "You" : "UI/UX Design Agent"}</strong>{message.taskType && <span className="task-chip">{message.taskType.replace("_", " ")}</span>}</div>
                <div className="message-body">
                    {isUser ? <p>{message.content}</p> : <ReactMarkdown rehypePlugins={[rehypeHighlight]}>{message.content}</ReactMarkdown>}
                </div>
                {!isUser && <button className="copy-button" onClick={copyMessage} type="button">{copied ? <Check size={14} /> : <Copy size={14} />}{copied ? "Copied" : "Copy"}</button>}
            </div>
        </article>
    );
}
