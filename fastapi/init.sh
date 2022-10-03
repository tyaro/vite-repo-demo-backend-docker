rm -r ./migration/versions/*
alembic revision --autogenerate -m "create tables"
alembic upgrade head
python main.py