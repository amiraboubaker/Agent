export type Message = { role: "user" | "assistant"; content: string; taskType?: string };

export type ChatResponse = { conversation_id: number; task_type: string; answer: string };
