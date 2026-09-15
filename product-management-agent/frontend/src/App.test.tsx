import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the product management workspace", async () => {
    render(<App />);
    expect(screen.getByText("Product Management Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we building")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the Product Management Agent/)).toBeInTheDocument();
});
