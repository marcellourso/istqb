import { useState } from 'react';

import type { Task } from '../api/apiClient';

export type TasksSectionProps = {
  tasks: Task[];
  onAddTask: (description: string) => Promise<void>;
  onToggleTask: (taskId: number, done: boolean) => Promise<void>;
};

export function TasksSection({ tasks, onAddTask, onToggleTask }: TasksSectionProps) {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  async function add(e: React.FormEvent) {
    e.preventDefault();
    if (!description.trim()) return;
    setLoading(true);
    try {
      await onAddTask(description);
      setDescription('');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card" data-testid="tasks-section">
      <div className="card__title">Tasks</div>

      <form className="row" onSubmit={add}>
        <input
          className="input"
          placeholder="Add a task…"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          data-testid="task-add-input"
        />
        <button className="button" type="submit" disabled={loading || !description.trim()} data-testid="task-add-submit">
          Add
        </button>
      </form>

      <div className="stack" data-testid="tasks-list">
        {tasks.length === 0 ? <div className="muted">No tasks</div> : null}
        {tasks.map((t) => (
          <label key={t.id} className="task" data-testid={`task-${t.id}`}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={(e) => onToggleTask(t.id, e.target.checked)}
              data-testid={`task-toggle-${t.id}`}
            />
            <span className={t.done ? 'task__text task__text--done' : 'task__text'}>{t.description}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
