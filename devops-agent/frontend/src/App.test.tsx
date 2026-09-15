import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the DevOps workspace", async () => {
    render(<App />);
    expect(screen.getByText("DevOps and Cloud Infrastructure Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we deploying")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the DevOps Agent/)).toBeInTheDocument();
});
