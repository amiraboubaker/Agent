import { useEffect, useState } from "react";
import { api } from "../services/api";
import type { Conversation, Message } from "../types";

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [conversationId, setConversationId] = useState<number>();
    const [isSending, setIsSending] = useState(false);
    const [error, setError] = useState<string>();

    useEffect(() => {
        api.conversations().then(setConversations).catch(() => undefined);
    }, []);

    async function sendMessage(content: string) {
        setIsSending(true);
        setError(undefined);
        setMessages((current) => [...current, { role: "user", content }]);
        try {
            const response = await api.chat(content, conversationId);
            setConversationId(response.conversation_id);
            setMessages((current) => [...current, { role: "assistant", content: response.answer, taskType: response.task_type }]);
            setConversations(await api.conversations());
        } catch (caught) {
            setError(caught instanceof Error ? caught.message : "Something went wrong.");
        } finally {
            setIsSending(false);
        }
    }

    function startNewConversation() {
        setConversationId(undefined);
        setMessages([]);
        setError(undefined);
    }

    return { messages, conversations, conversationId, isSending, error, sendMessage, startNewConversation };
}
