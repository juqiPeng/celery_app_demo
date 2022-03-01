from email.mime import base
from celery import shared_task, Task
import time

class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)

# 这里添加name参数以后，在其他地方不能使用相对导入的方式导入该方法，会抛出 NotRegistered 异常！！！
@shared_task(name="productor_app.add", bind=True, base=DebugTask)
def add(self, x, y):
    time.sleep(5)
    return x + y
