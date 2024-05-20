import django
django.setup()
import logging
import json
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta
from SituationAnalysis.models import Suggestion
from SituationAnalysis.tencent_chat import tencent_chat
from WiseSaying import settings
from WiseSaying.celery import app
# 获取logger实例
logger = logging.getLogger(__name__)


@app.task
def mytask():
    logger.info('进入定时任务')
    print('进入定时任务了')
    # 调用apihub中的接口，用于获取每月content_category1 数量最多的类型
    situation_url = '%s/%s/data' % (settings.situation_apihub_url, settings.path)
    response = requests.request("get", situation_url, timeout=5)
    info = response.text
    info_dict = json.loads(info)
    datas = info_dict["data"]
    if datas:
        analysis = datas[0]["content_category1"]
        logger.info('分类：%s' % analysis)
        month = datas[0]["month"]
        logger.info('月份：%s' % month)
        date_object = datetime.strptime(month, '%Y-%m')
        # 增加一个月
        next_month = date_object + relativedelta(months=1)
        next_month_str = next_month.strftime('%Y-%m')
        end_month = next_month_str + '-02 14:00:00'
        logging.info('end_month:%s' % end_month)
        text = ('上个月%s类的网络理政诉求较多，针对这一类型，在本月的工作报告中写出两点建议，供指导本月的工作方向。建议一，字数不得低于120个字，不得高于130个字，建议二，字数不得低于120个字，不得高于130个字') % analysis
        connect = '上个月%s类的网络理政诉求较多，针对这一类型，在本月的工作报告中写出两点建议，供指导本月的工作方向：' % analysis
        chat = tencent_chat(text)
        while not chat:
            chat = tencent_chat(text)
        info = connect + chat
        logger.info('info:%s' % info)
        # 存入数据库
        obj = Suggestion(month=end_month, suggestion=info)
        obj.save()
        logger.info('存入数据库成功')
    else:
        pass