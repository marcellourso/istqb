import { useState } from 'react';

export type CreateNoteFormProps = {
  onCreate: (payload: { title: string; content: string }) => Promise<void>;
};

export function CreateNoteForm({ onCreate }: CreateNoteFormProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await onCreate({ title, content });
      setTitle('');
      setContent('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card" onSubmit={submit} data-testid="create-note-form">
      <div className="card__title">New note</div>
      <label className="field">
        <div className="field__label">Title</div>
        <input
          className="input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
          data-testid="create-note-title"
        />
      </label>
      <label className="field">
        <div className="field__label">Content</div>
        <textarea
          className="textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={loading}
          rows={6}
          data-testid="create-note-content"
        />
      </label>
      {error ? <div className="error">{error}</div> : null}
      <button className="button button--primary" type="submit" disabled={loading || !title.trim() || !content.trim()} data-testid="create-note-submit">
        {loading ? 'Creating…' : 'Create'}
      </button>
    </form>
  );
}
