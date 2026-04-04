import { render, screen } from "@testing-library/react";
import { StatusBadge } from "../components/StatusBadge";

describe("StatusBadge", () => {
  it("renders the status text", () => {
    render(<StatusBadge status="Running" />);
    expect(screen.getByText("Running")).toBeInTheDocument();
  });

  it("renders unknown status without crashing", () => {
    render(<StatusBadge status="SomeUnknownState" />);
    expect(screen.getByText("SomeUnknownState")).toBeInTheDocument();
  });

  it("applies green colour for Running", () => {
    const { container } = render(<StatusBadge status="Running" />);
    const dot = container.querySelector("span > span") as HTMLElement;
    expect(dot.style.background).toBe("rgb(34, 197, 94)");
  });

  it("applies red colour for Error", () => {
    const { container } = render(<StatusBadge status="Error" />);
    const dot = container.querySelector("span > span") as HTMLElement;
    expect(dot.style.background).toBe("rgb(239, 68, 68)");
  });

  it("applies blue colour for Frozen", () => {
    const { container } = render(<StatusBadge status="Frozen" />);
    const dot = container.querySelector("span > span") as HTMLElement;
    expect(dot.style.background).toBe("rgb(96, 165, 250)");
  });
});
