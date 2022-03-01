# celery_app_demo

## 1. 介绍
这只是一个celery的demo项目，该项目演示了：

    1、如何将 celery 与 django 项目进行集成
    
    2、如何搭建生产者消费者模型，Django API 作为生产者，产生异步任务，消费者worker通过订阅队列的方式，对生产消息进行消费。

## 2. 使用方法

### 2.1 安装redis

建议采用docker方式

```shell
docker pull redis
```
```shell
docker run -d -p 6379:6379 redis
```

### 2.2 安装依赖
```shell
pip3 install -r requirements.txt
```

### 2.3 启动API服务
```shell
python manage.py runserver
```

### 2.4 打开命令行一：启动 productor worker
```shell
celery -A dj_celery worker -l info -Q productor_app.tasks.queue
```

### 2.5 打开命令行二：启动 consumer beat
```shell
celery -A consumer_app.celery_app beat
```

### 2.5 打开命令行三：启动 consumer worker
```shell
celery -A consumer_app.celery_app worker -l info -Q consumer_app.tasks.queue
```

## 3. 为什么启动两个worker？

对于这个项目中，consumer_app 文件夹中的内容应该不跟 DJANGO API 部署在同一台机器中，它应该是充当着消费者的角色，所以它部署在其他机器上，例如我们通常会将它部署在一些高性能计算节点中，去承担一些耗时耗力的计算任务。

而为什么我们的Django API 为啥呢也启了一个worker呢？ 因为有时候我们需要在 api 做一些异步操作的时候，可以使用这种方式做到 API 与一些操作解耦。

## 4. 观察

请求：http://127.0.0.1:8000/productor/

查看命令行，观察两个work的消费情况，理解celery的运行方式

