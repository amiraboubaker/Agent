import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the cybersecurity workspace", async () => {
    render(<App />);
    expect(screen.getByText("Cybersecurity Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we securing")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the Cybersecurity Agent/)).toBeInTheDocument();
});
