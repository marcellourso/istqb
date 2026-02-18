import type { Note } from '../api/apiClient';

export type NotesListProps = {
  notes: Note[];
  selectedNoteId: number | null;
  search: string;
  onSearchChange: (v: string) => void;
  onSelectNote: (noteId: number) => void;
};

export function NotesList({ notes, selectedNoteId, search, onSearchChange, onSelectNote }: NotesListProps) {
  const filtered = notes.filter((n) => {
    const q = search.trim().toLowerCase();
    if (!q) return true;
    return n.title.toLowerCase().includes(q) || n.content.toLowerCase().includes(q);
  });

  return (
    <div className="panel">
      <div className="panel__header">
        <div className="panel__title">Notes</div>
        <input
          className="input"
          placeholder="Search…"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          data-testid="notes-search"
        />
      </div>

      <div className="list" data-testid="notes-list">
        {filtered.length === 0 ? <div className="muted">No notes</div> : null}
        {filtered.map((n) => (
          <button
            key={n.id}
            className={`listItem ${selectedNoteId === n.id ? 'listItem--active' : ''}`}
            onClick={() => onSelectNote(n.id)}
            data-testid={`note-item-${n.id}`}
          >
            <div className="listItem__title">{n.title}</div>
            <div className="listItem__preview">{n.content.slice(0, 80)}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
