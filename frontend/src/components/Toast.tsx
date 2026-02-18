import './Toast.css';

export type ToastProps = {
  message: string;
  onClose: () => void;
};

export function Toast({ message, onClose }: ToastProps) {
  return (
    <div className="toast" role="status" data-testid="toast">
      <div className="toast__message">{message}</div>
      <button className="toast__close" onClick={onClose} data-testid="toast-close">
        ×
      </button>
    </div>
  );
}
