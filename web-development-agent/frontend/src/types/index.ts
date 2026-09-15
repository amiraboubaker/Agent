export type TaskType = "requirements" | "architecture" | "ui" | "frontend" | "backend" | "database" | "testing" | "deployment" | "general_web";

export type Message = {
    role: "user" | "assistant";
    content: string;
    taskType?: TaskType;
};

export type Conversation = {
    id: number;
    title: string;
    task_type: TaskType;
    created_at: string;
    updated_at: string;
    message_count: number;
};

export type ChatResponse = {
    conversation_id: number;
    task_type: TaskType;
    answer: string;
    created_at: string;
};
