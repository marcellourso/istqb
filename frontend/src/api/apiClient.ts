export type Note = {
  id: number;
  title: string;
  content: string;
  created_at: string;
};

export type Task = {
  id: number;
  note_id: number;
  description: string;
  done: boolean;
  created_at: string;
};

export type AnalysisMode = 'rules' | 'ai';

export type AnalysisResult = {
  mode: AnalysisMode;
  summary: string;
  priority: 'low' | 'medium' | 'high';
  tasks: string[];
};

export type NoteDetail = {
  id: number;
  title: string;
  content: string;
  created_at: string;
  tasks: Task[];
  latest_analysis: AnalysisResult | null;
};

export class ApiError extends Error {
  status: number;
  body?: unknown;

  constructor(message: string, status: number, body?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

function hasDetail(body: unknown): body is { detail: unknown } {
  return typeof body === 'object' && body !== null && 'detail' in body;
}

const baseUrl = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? '';

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${baseUrl}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  let body: unknown = undefined;
  const contentType = res.headers.get('content-type') ?? '';
  if (contentType.includes('application/json')) {
    body = await res.json();
  } else {
    body = await res.text();
  }

  if (!res.ok) {
    const msg = hasDetail(body) ? String(body.detail) : `HTTP ${res.status}`;
    throw new ApiError(msg, res.status, body);
  }

  return body as T;
}

export async function listNotes(): Promise<Note[]> {
  return apiFetch<Note[]>('/notes');
}

export async function createNote(payload: { title: string; content: string }): Promise<Note> {
  return apiFetch<Note>('/notes', { method: 'POST', body: JSON.stringify(payload) });
}

export async function getNote(noteId: number): Promise<NoteDetail> {
  return apiFetch<NoteDetail>(`/notes/${noteId}`);
}

export async function addTask(noteId: number, payload: { description: string }): Promise<Task> {
  return apiFetch<Task>(`/notes/${noteId}/tasks`, { method: 'POST', body: JSON.stringify(payload) });
}

export async function toggleTask(taskId: number, payload: { done: boolean }): Promise<Task> {
  return apiFetch<Task>(`/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify(payload) });
}

export async function analyzeNote(noteId: number, mode: AnalysisMode): Promise<AnalysisResult> {
  const query = new URLSearchParams({ mode });
  return apiFetch<AnalysisResult>(`/notes/${noteId}/analyze?${query.toString()}`, { method: 'POST' });
}
