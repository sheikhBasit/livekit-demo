.PHONY: up down build dev-server dev-client install

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

install:
	cd server && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
	cd client && npm install

dev-server:
	cd server && .venv/bin/uvicorn main:app --reload --port 8001

dev-client:
	cd client && npm run dev
