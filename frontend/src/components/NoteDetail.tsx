import type { NoteDetail } from '../api/apiClient';

import { AnalysisSection } from './AnalysisSection';
import { TasksSection } from './TasksSection';

export type NoteDetailProps = {
  note: NoteDetail;
  loadingAnalysis: boolean;
  onAddTask: (description: string) => Promise<void>;
  onToggleTask: (taskId: number, done: boolean) => Promise<void>;
  onAnalyze: (mode: 'rules' | 'ai') => Promise<void>;
};

export function NoteDetail({ note, loadingAnalysis, onAddTask, onToggleTask, onAnalyze }: NoteDetailProps) {
  return (
    <div className="panel" data-testid="note-detail">
      <div className="panel__header">
        <div className="panel__title" data-testid="note-title">
          {note.title}
        </div>
      </div>

      <div className="card">
        <div className="smallTitle">Content</div>
        <pre className="content" data-testid="note-content">
{note.content}
        </pre>
      </div>

      <TasksSection tasks={note.tasks} onAddTask={onAddTask} onToggleTask={onToggleTask} />

      <AnalysisSection latest={note.latest_analysis} onAnalyze={onAnalyze} loading={loadingAnalysis} />
    </div>
  );
}
