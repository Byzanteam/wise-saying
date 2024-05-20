import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
# 设置celery的环境变量和django-celery的工作目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WiseSaying.settings")
# 实例化celery应用，传入服务器名称
app = Celery("WiseSaying")
# 加载celery配置
app.config_from_object("django.conf:settings")
# 如果在项目中，创建了task.py,那么celery就会沿着app去查找task.py来生成任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# 手动导入并注册你的任务
from SituationAnalysis.task import mytask
app.register_task(mytask)

# # 定义定时任务调度
app.conf.beat_schedule = {
    'execute-every-minute': {
        'task': 'SituationAnalysis.task.mytask',
        'schedule': crontab(day_of_month='1', minute=0, hour=0),  # 每个月的1号执行
    },
}