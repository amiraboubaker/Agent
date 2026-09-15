import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App";

vi.mock("./services/api", () => ({ api: { conversations: vi.fn().mockResolvedValue([]), chat: vi.fn() } }));

test("renders the data science workspace", async () => {
    render(<App />);
    expect(screen.getByText("Data Science Agent")).toBeInTheDocument();
    expect(screen.getByText("What are we exploring")).toBeInTheDocument();
    expect(await screen.findByPlaceholderText(/Ask the Data Science Agent/)).toBeInTheDocument();
});
