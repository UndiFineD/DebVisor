# DebVisor Makefile - Build, test, and deployment automation
# Usage: make [target]

.PHONY: help build test deploy clean install-deps setup-db protoc lint format run-rpc run-panel

# Configuration
PYTHON := python3
PIP := pip3
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
PROTOC := protoc

# Paths
RPC_DIR := opt/services/rpc
PANEL_DIR := opt/web/panel
PROTO_DIR := opt/services/rpc/proto
BUILD_DIR := build
DIST_DIR := dist

.PHONY: help
help:
	@echo "DebVisor Makefile - Build and deployment automation"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help              Show this help message"
	@echo "  build             Build all components"
	@echo "  install-deps      Install Python dependencies"
	@echo "  setup-db          Setup database (PostgreSQL)"
	@echo "  protoc            Compile Protocol Buffer files"
	@echo "  lint              Run code linting"
	@echo "  format            Format code with Black"
	@echo "  test              Run unit tests"
	@echo "  test-coverage     Run tests with coverage"
	@echo "  test-integration  Run integration tests"
	@echo "  run-rpc           Run RPC service locally"
	@echo "  run-panel         Run web panel locally"
	@echo "  deploy-rpc        Deploy RPC service to systemd"
	@echo "  deploy-panel      Deploy web panel to systemd"
	@echo "  deploy-all        Deploy all services"
	@echo "  clean             Remove build artifacts"
	@echo "  docker-build      Build Docker images"
	@echo "  docker-up         Start Docker containers"
	@echo "  docker-down       Stop Docker containers"

.PHONY: install-deps
install-deps:
	@echo "Installing Python dependencies..."
	$(PIP) install -r $(RPC_DIR)/requirements.txt
	$(PIP) install -r $(PANEL_DIR)/requirements.txt
	@echo "Dependencies installed successfully"

.PHONY: protoc
protoc:
	@echo "Compiling Protocol Buffer files..."
	cd $(RPC_DIR) && $(PROTOC) --python_out=. --grpc_python_out=. proto/*.proto
	@echo "Protocol buffers compiled successfully"

.PHONY: lint
lint:
	@echo "Running code linting..."
	$(FLAKE8) $(RPC_DIR) --max-line-length=120 --ignore=E501,W503
	$(FLAKE8) $(PANEL_DIR) --max-line-length=120 --ignore=E501,W503
	@echo "Linting complete"

.PHONY: format
format:
	@echo "Formatting code with Black..."
	$(BLACK) $(RPC_DIR) --line-length=120
	$(BLACK) $(PANEL_DIR) --line-length=120
	@echo "Code formatting complete"

.PHONY: test
test:
	@echo "Running unit tests..."
	$(PYTEST) tests/ -v --tb=short
	@echo "Tests complete"

.PHONY: test-coverage
test-coverage:
	@echo "Running tests with coverage..."
	$(PYTEST) tests/ -v --cov=$(RPC_DIR) --cov=$(PANEL_DIR) --cov-report=html
	@echo "Coverage report generated in htmlcov/"

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	$(PYTEST) tests/integration/ -v --tb=short
	@echo "Integration tests complete"

.PHONY: run-rpc
run-rpc:
	@echo "Starting RPC service..."
	cd $(RPC_DIR) && $(PYTHON) server.py --config config.json --debug

.PHONY: run-panel
run-panel:
	@echo "Starting web panel..."
	cd $(PANEL_DIR) && $(PYTHON) -m flask run --host=0.0.0.0 --port=5000 --reload

.PHONY: setup-db
setup-db:
	@echo "Setting up database..."
	cd $(PANEL_DIR) && $(PYTHON) -c "from app import create_app, db; app = create_app('development'); app.app_context().push(); db.create_all(); print('Database setup complete')"

.PHONY: build
build: install-deps protoc lint
	@echo "Build complete"

.PHONY: deploy-rpc
deploy-rpc:
	@echo "Deploying RPC service..."
	sudo cp $(RPC_DIR)/systemd/rpc.service /etc/systemd/system/debvisor-rpc.service
	sudo systemctl daemon-reload
	sudo systemctl enable debvisor-rpc.service
	sudo systemctl restart debvisor-rpc.service
	@echo "RPC service deployed"

.PHONY: deploy-panel
deploy-panel:
	@echo "Deploying web panel..."
	sudo cp $(PANEL_DIR)/systemd/panel.service /etc/systemd/system/debvisor-panel.service
	sudo cp $(PANEL_DIR)/nginx/panel.conf /etc/nginx/sites-available/debvisor-panel
	sudo ln -sf /etc/nginx/sites-available/debvisor-panel /etc/nginx/sites-enabled/debvisor-panel
	sudo systemctl daemon-reload
	sudo systemctl enable debvisor-panel.service
	sudo systemctl restart debvisor-panel.service
	sudo nginx -t && sudo systemctl restart nginx
	@echo "Web panel deployed"

.PHONY: deploy-all
deploy-all: deploy-rpc deploy-panel
	@echo "All services deployed successfully"

.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -delete
	rm -rf build dist htmlcov .pytest_cache .coverage
	@echo "Clean complete"

.PHONY: docker-build
docker-build:
	@echo "Building Docker images..."
	docker build -t debvisor-rpc:latest -f $(RPC_DIR)/Dockerfile $(RPC_DIR)
	docker build -t debvisor-panel:latest -f $(PANEL_DIR)/Dockerfile $(PANEL_DIR)
	@echo "Docker build complete"

.PHONY: docker-up
docker-up:
	@echo "Starting Docker containers..."
	docker-compose -f docker-compose.yml up -d
	@echo "Containers started"

.PHONY: docker-down
docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f docker-compose.yml down
	@echo "Containers stopped"

.PHONY: docker-logs
docker-logs:
	docker-compose -f docker-compose.yml logs -f

.PHONY: status
status:
	@echo "=== DebVisor Services Status ==="
	@echo ""
	@echo "RPC Service:"
	@sudo systemctl status debvisor-rpc.service || echo "Not running"
	@echo ""
	@echo "Web Panel:"
	@sudo systemctl status debvisor-panel.service || echo "Not running"
	@echo ""
	@echo "Nginx:"
	@sudo systemctl status nginx || echo "Not running"

.PHONY: logs
logs:
	@echo "RPC Service Logs:"
	sudo journalctl -u debvisor-rpc.service -f &
	@echo "Web Panel Logs:"
	sudo journalctl -u debvisor-panel.service -f

.PHONY: restart
restart:
	@echo "Restarting all services..."
	sudo systemctl restart debvisor-rpc.service
	sudo systemctl restart debvisor-panel.service
	sudo systemctl restart nginx
	@echo "Services restarted"

.PHONY: stop
stop:
	@echo "Stopping all services..."
	sudo systemctl stop debvisor-rpc.service
	sudo systemctl stop debvisor-panel.service
	@echo "Services stopped"

.PHONY: start
start:
	@echo "Starting all services..."
	sudo systemctl start debvisor-rpc.service
	sudo systemctl start debvisor-panel.service
	@echo "Services started"

.DEFAULT_GOAL := help