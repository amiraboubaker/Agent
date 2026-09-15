import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the web development workspace", async () => {
    render(<App />);
    expect(screen.getByText("Web Development Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we building")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the Web Development Agent/)).toBeInTheDocument();
});
