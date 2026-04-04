import { render, screen, fireEvent } from "@testing-library/react";
import { ConfirmDialog } from "../components/ConfirmDialog";

describe("ConfirmDialog", () => {
  const baseProps = {
    open: true,
    title: "Delete container",
    message: "This action cannot be undone.",
    onConfirm: vi.fn(),
    onCancel: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders nothing when closed", () => {
    const { container } = render(<ConfirmDialog {...baseProps} open={false} />);
    expect(container.firstChild).toBeNull();
  });

  it("renders title and message when open", () => {
    render(<ConfirmDialog {...baseProps} />);
    expect(screen.getByText("Delete container")).toBeInTheDocument();
    expect(screen.getByText("This action cannot be undone.")).toBeInTheDocument();
  });

  it("calls onConfirm when confirm button clicked", () => {
    render(<ConfirmDialog {...baseProps} />);
    fireEvent.click(screen.getByText("Confirm"));
    expect(baseProps.onConfirm).toHaveBeenCalledTimes(1);
  });

  it("calls onCancel when cancel button clicked", () => {
    render(<ConfirmDialog {...baseProps} />);
    fireEvent.click(screen.getByText("Cancel"));
    expect(baseProps.onCancel).toHaveBeenCalledTimes(1);
  });

  it("uses custom confirmLabel when provided", () => {
    render(<ConfirmDialog {...baseProps} confirmLabel="Delete" />);
    expect(screen.getByText("Delete")).toBeInTheDocument();
  });
});
