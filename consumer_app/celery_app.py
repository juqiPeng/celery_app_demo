from celery import Celery
import time
import datetime
from celery.schedules import crontab

app = Celery(broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/0")

# 指定task进入到哪个队列中
app.conf.task_routes = {
    'consumer_app.*': {
        'queue': 'consumer_app.tasks.queue'
    },
    'productor_app.*': {
        'queue': 'productor_app.tasks.queue'
    }
}
app.autodiscover_tasks()


# 定时任务demo，每间一分钟将会执行一次
app.conf.beat_schedule = {
    "each1m_task": {
        "task": "consumer_app.timer",
        'schedule':crontab(minute='*/1')
    }
}


# 消费者task，比如一些耗时耗力的 AI 计算，我们会将其放在这里面
# 并且将 consumer_app 跟 API 服务分离部署到不同的机器中
@app.task(name="consumer_app.doing_task", bind=True)
def doing_task(self, x, y):
    time.sleep(5)
    return f"##################{x+y}####################"


@app.task(name="consumer_app.timer")
def time_teller():
    print("------Scheduled task is executing-------")
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")