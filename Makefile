.PHONY: runserver
runserver:
	@echo "Starting the Django development server..."
	python manage.py runserver 0.0.0.0:8000

.PHONY: migrations
migrations:
	@echo "Creating new database migrations..."
	python manage.py makemigrations

.PHONY: migrate
migrate:
	@echo "Applying database migrations..."
	python manage.py migrate

.PHONY: app
app:
	@echo "Creating a new app..."
	python manage.py startapp $(name)


.PHONY: static
static:
	@echo "Collecting static files..."
	python3 manage.py collectstatic --noinput

.PHONY: sync
sync:
	@echo "Running database migrations and synchronizing database schema..."
	python manage.py migrate --run-syncdb

.PHONY: kill
kill:
	@echo "Killing the process running on port 8000..."
	sudo fuser -k 8000/tcp

.PHONY: admin
admin:
	@echo "Creating a superuser..."
	python manage.py createsuperuser

.PHONY: test
test:
	@echo "Running the project's tests..."
	python manage.py test

.PHONY: activate
activate:
	@echo "Activating the Pipenv shell..."
	pipenv shell

.PHONY: shell
shell:
	@echo "Starting the Django shell..."
	python manage.py shell