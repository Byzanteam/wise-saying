from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models
from .models import Suggestion


class FormDataView(APIView):
    def get(self,request):
        exists = models.Suggestion.objects.filter(Q(month='2024-04-02 14:00:00') | Q(month='2024-05-02 14:00:00')).exists()
        if not exists:
            # 如果不存在，插入两条新数据
            suggestion1 = models.Suggestion(month='2024-04-02 14:00:00',suggestion='上个月住房保障与房地产管理类的网络理政诉求较多，针对这一类型，在本月的工作报告中写出两点建议，供指导本月的工作方向：建议一：针对住房保障与房地产管理类的网络理政诉求，应加强相关政策宣传，提高公众对政策的理解和认知，减少误解和不满。同时，建立健全住房保障体系，加大对中低收入家庭的住房保障力度，确保政策的公平性和有效性。 建议二：为了更好地解决住房保障与房地产管理类的网络理政诉求，应加强与相关部门的协作，形成工作合力，提高问题处理效率。同时，建立完善的房地产市场监管机制，打击违法违规行为，维护市场秩序，保障消费者权益。')
            suggestion1.save()
            suggestion2 = models.Suggestion(month='2024-05-02 14:00:00',suggestion='上个月住房保障与房地产管理类的网络理政诉求较多，针对这一类型，在本月的工作报告中写出两点建议，供指导本月的工作方向：建议一： 为了缓解住房保障与房地产管理类的网络理政诉求，我们建议在加强对房地产市场的监管的同时，也需注重保障和改善民生。具体措施包括：适度调整政策，引导房地产市场健康稳定发展；优化保障性住房供应体系，满足更多低收入家庭的住房需求；加大对房地产市场的信息披露力度，提高市场透明度，以促进公平正义。 建议二： 此外，我们还需要加强网络理政平台的建设和完善。一方面，提高网络理政平台的技术水平，包括信息处理、数据分析和智能化辅助决策等方面，以提高工作效率和精准度。另一方面，提升网络理政平台的服务质量，加强对工作人员的业务培训，提高对舆情的敏锐度和对民众诉求的响应速度。同时，加强与其他相关部门的协调配合，形成工作合力，以更好地解决住房保障与房地产管理类的问题。')
            suggestion2.save()
        else:
            pass
        data = Suggestion.objects.all()
        results = {
            'meta': {
                'errcode': 0,
                'errmsg': '成功',
                'status_code': 200
            },
            'data': []
        }
        data_list = list(data)  # 将 QuerySet 转换为列表
        for obj in data_list:
            result_item = {
                'month': obj.month,
                'suggestion': obj.suggestion
            }
            results['data'].append(result_item)
        return JsonResponse(results)



