export type TaskType = "data_quality" | "eda" | "visualization" | "statistics" | "modeling" | "general_analysis";

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
