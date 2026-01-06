Docker development notes

Quick start (development):

1. Build image and start the container:

   docker compose up --build

2. The web app will be available at http://localhost:8000

Notes:
- The compose file mounts the project dir into the container for fast iteration.
- Static files will be collected by the container entrypoint into `/app/staticfiles`.
- Use `docker compose run web python manage.py test` to run the test suite inside the container.

Production notes:
- Consider using a managed Postgres instance and update `DATABASES` accordingly.
- Set `DEBUG=0` and provide a secure `SECRET_KEY` via env.
- Use an external volume for media files.
