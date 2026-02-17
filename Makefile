.PHONY: setup run-backend run-frontend test lint e2e

setup:
	@echo "TODO: setup backend (venv + deps) e frontend (npm install)"

run-backend:
	@. backend/.venv/bin/activate 2>/dev/null || (echo "Backend venv mancante. Esegui: make setup" && exit 1)
	@. backend/.venv/bin/activate && uvicorn app.main:app --reload

run-frontend:
	@echo "TODO: avvio React dev server" 
	@echo "Suggerimento: cd frontend && npm install && npm run dev"
	@exit 1

test:
	@. backend/.venv/bin/activate 2>/dev/null || (echo "Backend venv mancante. Esegui: make setup" && exit 1)
	@. backend/.venv/bin/activate && (cd backend && pytest)

lint:
	@echo "TODO: backend ruff/mypy + frontend lint"
	@exit 1

e2e:
	@echo "TODO: playwright"
	@exit 1
