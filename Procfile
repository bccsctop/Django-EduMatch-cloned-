web: daphne edumatch.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: REMAP_SIGTERM=SIGQUIT celery worker --app edumatch.celery.app --loglevel info