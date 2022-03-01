from rest_framework.views import APIView
from productor_app.tasks import add
from rest_framework.response import Response
from dj_celery.celery_app import app


# Submit asynchronous task API
class ProductorView(APIView):

    def get(self, request, *args, **kwargs):
        task1 = add.delay(12,13)
        task2 = add.apply_async(args=[100, 200])

        # This task theory is to run in the consumer app
        task3 = app.send_task("consumer_app.doing_task", args=[300, 500], queue="consumer_app.tasks.queue")
        task4 = app.send_task("consumer_app.doing_task", args=[1000, 500])
        result = {
            "msg":"异步任务已下发",
            "task_id_1": task1.id,
            "task_id_2": task2.id,
            "task_id_3": task3.id,
            "task_id_4": task4.id
        }
        return Response(result)
