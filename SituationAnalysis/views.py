import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from WiseSaying import settings
from rest_framework.views import APIView
from .tencent_chat import tencent_chat


class FormDataView(APIView):
    @csrf_exempt
    def get(self,request):
        month = request.GET.get('month')
        print(month)
        if month:
            # 调用apihub中的接口，用于获取content_category1 数量最多的类型
            situation_url = '%s/%s/data?month=%s' % (settings.situation_apihub_url,settings.path, month)
            response = requests.request("get", situation_url)
            info = response.text
            info_dict = json.loads(info)
            try:
                # 尝试获取 content_category1 字段的值
                type_value = info_dict["data"][0]["content_category1"]
            except (KeyError, IndexError):
                # 如果无法获取到值，则将 type_value 设为 None
                type_value = None
            if type_value:
                text = ('上个月%s类的网络理政诉求较多，针对这一类型，在本月的工作报告中写出两点建议，供指导本月的工作方向。两点建议的字数，分别限制在120字左右'
                        '参考文本:春节将至，拖欠工资的诉求持续增多，为确保不发生因欠薪引发群体性事件，请相关职能部门收到诉求后做到及时处理、'
                        '及时控制、及时解决、及时消除群体性突发事件的各种诱因，防止矛盾激化和事态扩大。各部门应进一步加强配合协作力度，'
                        '充分发挥各自职能职责，在保障农民工工资及工程款支付工作中形成分工协作、齐抓共管、综合治理的整体合力，推动工作有效实施。') % type_value
                chat = tencent_chat(text)
                return JsonResponse({'code': 200, 'msg': chat})
            else:
                return JsonResponse({'code': 200, 'msg': "表中并没有%s的数据" % month})
        else:
            return JsonResponse({'code': 200, 'msg':"请传参数month!"})



