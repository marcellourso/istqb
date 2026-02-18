import { useCallback, useEffect, useMemo, useState } from 'react';

import { ApiError, analyzeNote, createNote, getNote, listNotes, addTask, toggleTask, type Note, type NoteDetail, type AnalysisMode } from './api/apiClient';
import { CreateNoteForm } from './components/CreateNoteForm';
import { NoteDetail as NoteDetailView } from './components/NoteDetail';
import { NotesList } from './components/NotesList';
import { Toast } from './components/Toast';

import './App.css';

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNoteId, setSelectedNoteId] = useState<number | null>(null);
  const [noteDetail, setNoteDetail] = useState<NoteDetail | null>(null);
  const [search, setSearch] = useState('');

  const [loadingNotes, setLoadingNotes] = useState(false);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [toast, setToast] = useState<string | null>(null);

  const refreshNotes = useCallback(async () => {
    setError(null);
    setLoadingNotes(true);
    try {
      const items = await listNotes();
      setNotes(items);
      if (selectedNoteId === null && items.length > 0) {
        setSelectedNoteId(items[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoadingNotes(false);
    }
  }, [selectedNoteId]);

  async function refreshSelectedNote(noteId: number) {
    setError(null);
    setLoadingDetail(true);
    try {
      const detail = await getNote(noteId);
      setNoteDetail(detail);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setNoteDetail(null);
    } finally {
      setLoadingDetail(false);
    }
  }

  useEffect(() => {
    void refreshNotes();
  }, [refreshNotes]);

  useEffect(() => {
    if (selectedNoteId === null) {
      setNoteDetail(null);
      return;
    }
    void refreshSelectedNote(selectedNoteId);
  }, [selectedNoteId]);

  const selectedTitle = useMemo(() => {
    if (selectedNoteId === null) return null;
    return notes.find((n) => n.id === selectedNoteId)?.title ?? null;
  }, [notes, selectedNoteId]);

  async function handleCreateNote(payload: { title: string; content: string }) {
    const created = await createNote(payload);
    await refreshNotes();
    setSelectedNoteId(created.id);
  }

  async function handleAddTask(description: string) {
    if (selectedNoteId === null) return;
    await addTask(selectedNoteId, { description });
    await refreshSelectedNote(selectedNoteId);
  }

  async function handleToggleTask(taskId: number, done: boolean) {
    if (selectedNoteId === null) return;
    await toggleTask(taskId, { done });
    await refreshSelectedNote(selectedNoteId);
  }

  async function handleAnalyze(mode: AnalysisMode) {
    if (selectedNoteId === null) return;

    setLoadingAnalysis(true);
    try {
      await analyzeNote(selectedNoteId, mode);
      await refreshSelectedNote(selectedNoteId);
    } catch (err) {
      if (err instanceof ApiError && err.status === 501) {
        setToast('AI mode not implemented yet');
        return;
      }
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoadingAnalysis(false);
    }
  }

  return (
    <div className="app">
      {toast ? <Toast message={toast} onClose={() => setToast(null)} /> : null}

      <header className="topbar">
        <div className="topbar__title" data-testid="app-title">
          Notes Analyzer
        </div>
        <div className="topbar__right">
          {loadingNotes ? <span className="muted">Loading…</span> : null}
        </div>
      </header>

      {error ? (
        <div className="banner banner--error" role="alert">
          {error}
        </div>
      ) : null}

      <main className="layout">
        <aside className="left">
          <CreateNoteForm onCreate={handleCreateNote} />
          <NotesList
            notes={notes}
            selectedNoteId={selectedNoteId}
            search={search}
            onSearchChange={setSearch}
            onSelectNote={(id) => setSelectedNoteId(id)}
          />
        </aside>

        <section className="right">
          {selectedNoteId === null ? (
            <div className="panel">
              <div className="muted" data-testid="note-empty-state">
                Create a note to get started.
              </div>
            </div>
          ) : loadingDetail ? (
            <div className="panel">
              <div className="muted">Loading note…</div>
            </div>
          ) : noteDetail ? (
            <NoteDetailView
              note={noteDetail}
              loadingAnalysis={loadingAnalysis}
              onAddTask={handleAddTask}
              onToggleTask={handleToggleTask}
              onAnalyze={handleAnalyze}
            />
          ) : (
            <div className="panel">
              <div className="muted">Note not found{selectedTitle ? `: ${selectedTitle}` : ''}</div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
