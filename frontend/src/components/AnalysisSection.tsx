import type { AnalysisResult, AnalysisMode } from '../api/apiClient';

export type AnalysisSectionProps = {
  latest: AnalysisResult | null;
  onAnalyze: (mode: AnalysisMode) => Promise<void>;
  loading: boolean;
};

function priorityClass(p: AnalysisResult['priority']): string {
  if (p === 'high') return 'badge badge--red';
  if (p === 'medium') return 'badge badge--yellow';
  return 'badge badge--gray';
}

export function AnalysisSection({ latest, onAnalyze, loading }: AnalysisSectionProps) {
  return (
    <div className="card" data-testid="analysis-section">
      <div className="card__title">Analysis</div>

      <div className="row">
        <button className="button button--primary" onClick={() => onAnalyze('rules')} disabled={loading} data-testid="analyze-rules-btn">
          Analyze (rules)
        </button>
        <button className="button" onClick={() => onAnalyze('ai')} disabled={loading} data-testid="analyze-ai-btn">
          Analyze (AI mode)
        </button>
      </div>

      <div className="card" data-testid="analysis-result">
        {!latest ? (
          <div className="muted">No analysis yet</div>
        ) : (
          <>
            <div className="row row--wrap">
              <span className="badge" data-testid="analysis-mode">mode: {latest.mode}</span>
              <span className={priorityClass(latest.priority)} data-testid="analysis-priority">
                priority: {latest.priority}
              </span>
            </div>

            <div className="stack">
              <div>
                <div className="smallTitle">Summary</div>
                <div data-testid="analysis-summary">{latest.summary}</div>
              </div>
              <div>
                <div className="smallTitle">Suggested tasks</div>
                <div className="stack" data-testid="analysis-tasks">
                  {latest.tasks.length === 0 ? <div className="muted">None</div> : null}
                  {latest.tasks.map((t, idx) => (
                    <div key={idx} className="mono">
                      - {t}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
