web: daphne edumatch.asgi:application --port $PORT --bind 0.0.0.0 
worker: REMAP_SIGTERM=SIGQUIT celery worker --app edumatch.celery.app --loglevel info