import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the UI/UX design workspace", async () => {
    render(<App />);
    expect(screen.getByText("UI/UX Design Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we designing")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the UI\/UX Design Agent/)).toBeInTheDocument();
});
