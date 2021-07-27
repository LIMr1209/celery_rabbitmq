from celery_pro import app

@app.task
def add(x, y):
    return x + y