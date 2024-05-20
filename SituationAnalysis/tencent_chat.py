import json
import re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
from WiseSaying import settings
import logging
# logger = logging.getLogger('api')


def tencent_chat(text):
    try:
        APPID = settings.APPID
        APPSECRET = settings.APPSECRET
        cred = credential.Credential(APPID, APPSECRET)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)
        req = models.ChatStdRequest()
        params = {
            "Messages": [
                {
                    "Role": "user",
                    "Content": text
                }
            ]
        }
        req.from_json_string(json.dumps(params))
        resp = client.ChatStd(req)
        # 循环遍历每个字典，解析data字段中的JSON数据，提取content内容
        sentence = ''.join([json.loads(event['data'])['Choices'][0]['Delta']['Content'] for event in resp])
        # 使用正则表达式去除多余空格，并保留特定格式
        formatted_text = re.sub(r'\s+', ' ', sentence.replace(" ", "")).strip()
        logging.info('已成功拿到数据')
        logging.debug('这是tencent_chat.py')
        return formatted_text
    except TencentCloudSDKException as err:
        print(err)