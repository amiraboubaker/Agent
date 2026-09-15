import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("Mobile Application Development Agent", () => {
  it("renders the project planning workspace", () => {
    render(<App />);
    expect(screen.getByText(/Make the next/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Describe the app/i)).toBeInTheDocument();
  });
});
