import type { ChatResponse, Conversation } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "The API request failed.");
    }
    return response.json() as Promise<T>;
}

export const api = {
    chat: (message: string, conversationId?: number) =>
        request<ChatResponse>("/chat", {
            method: "POST",
            body: JSON.stringify({ message, conversation_id: conversationId }),
        }),
    conversations: () => request<Conversation[]>("/conversations"),
};
