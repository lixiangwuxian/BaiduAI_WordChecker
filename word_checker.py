import requests
import json
import time

class Word_checker:
    def __init__(self,API_key,Secret_key):
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        access_token = self.get_token(API_key,Secret_key)
        self.full_request_url = request_url + "?access_token=" + access_token
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
    def get_token(self,API_key,Secret_key)->str:
        url = "https://aip.baidubce.com/oauth/2.0/token?client_id="+API_key+"&client_secret="+Secret_key+"&grant_type=client_credentials"
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['access_token']
    def check_word(self,answer:str)->dict:
        if answer=='':
            return {
                'state':1,
                'msg':'未触发过滤'
            }
        params ={"text":answer}
        result={}
        while result.get('conclusionType') is None:
            if result.get('error_code')!=None and result.get('error_code')!=18:#if not qos limit and not empty request
                raise Exception("API Error:"+result.get('error_code').__str__())
            response = requests.post(self.full_request_url, data=params, headers=self.headers)
            result=response.json()
            time.sleep(0.1)
        if result.get('conclusionType')==1:
            return {
                'state':result.get('conclusionType'),
                'msg':'未触发过滤'
            }
        else:
            return {#返回第一个触发原因
                'state':result.get('conclusionType'),
                'msg':result.get('data')[0].get('msg'),
                'sub_type':result.get('data')[0].get('subType')
            }
    def word_replace(self,text:str)->str:
        result=self.check_word(text)
        if result["state"]!=1:
            print(result["msg"])
            print(text)
            return "这个问题可能并不适合回答，我们还是换个话题吧。触发原因："+result["sub_type"].__str__()
        else:
            print("审核结果："+result["msg"])
            return text

if __name__=='__main__':
    API_key="Sosjmn1Shu0DdUiD4hmwangl"#改成你的
    Secret_key="czyXq4vmE5OKfcjNtm11HahAu54OpHih"
    c=Word_checker(API_key,Secret_key)
    print(c.check_word("*******"))
    print(c.word_replace("*******"))