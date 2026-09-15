import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the AI workspace", async () => {
    render(<App />);
    expect(screen.getByText("AI and Machine Learning Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the AI Agent/)).toBeInTheDocument();
});
