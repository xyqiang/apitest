from tests.api.httpbin import * 


# 第一个单元测试
def test_version():
    from apitest import __version__
    assert isinstance(__version__,str)

# import requests

# class BaseApi(object):

#     method = "get"
#     url = ""
#     params = {}
#     headers = {}
#     data = {}
#     json = {}

#     def set_params(self,**params):
#         self.params = {}
#         return self
    
#     def set_data(self,data):
#         self.data = data
#         return self

#     def set_json(self,json_data):
#         self.json = json_data
#         return self

#     def run(self):
#         self.responce = requests.request(self.method,self.url,params=self.params,headers=self.headers,data=self.data,json=self.json)
#         return self

#     def validate(self,key,value):
#         actual_value = getattr(self.responce,key)
#         assert actual_value == value
#         return self   
    

# class ApiHttpbinGet(BaseApi):
    
#     url = "https://httpbin.org/get"
#     params = {}
#     method = "GET"
#     headers = {"Accept": "application/json"}
#     data = ""
#     json = {}

    # def set_params(self,**params):
    #     self.params = {}
    #     return self

    # def run(self):
    #     self.responce = requests.request(self.method,self.url,params=self.params,headers=self.headers,data=self.data,json=self.json)
    #     return self

    # def validate(self,key,value):
    #     actual_value = getattr(self.responce,key)
    #     assert actual_value == value
    #     return self

# class ApiHttpbinPost(BaseApi):
    
#     url = "https://httpbin.org/post"
#     method = "POST"
#     headers = {"Accept": "application/json"}
#     json = {"xyq":18}

    # def run(self):
    #     self.responce = requests.request(self.method,self.url,headers=self.headers,json=self.json)
    #     return self   

    # def validate(self,key,value):
    #     actual_value = getattr(self.responce,key)
    #     assert actual_value == value
    #     return self



def test_httpbin_get():
    # resp = requests.get("https://httpbin.org/get")
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "https://httpbin.org/get"

    ApiHttpbinGet()\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/get")\
        .validate("json().args",{})\
        .validate("json().headers.Accept","application/json")
    

def test_httpbin_get_with_params():
    # resp = requests.get(
    #     "https://httpbin.org/get",
    #     params={"xyq":18},
    # )
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "https://httpbin.org/get?xyq=18"

    ApiHttpbinGet()\
        .set_params(xyq=18,lqm=15)\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/get?xyq=18&lqm=15")\
        .validate("json().headers.Accept","application/json")

def test_httpbin_post():
    # resp = requests.post(
    #     "https://httpbin.org/post",
    #     json={"xyq":18}
    #     )
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "https://httpbin.org/post"
    # assert resp.json()["json"]["xyq"] == 18 

    ApiHttpbinPost()\
        .set_json({"xyq":18})\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/post")\
        .validate("json().headers.Accept","application/json")\
        .validate("json().json.xyq",18)

def test_httpbin_parameters_share():
    user_id = "xyq18"
    ApiHttpbinGet()\
        .set_params(user_id=user_id)\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/get?user_id={}".format(user_id))\
        .validate("json().headers.Accept","application/json")


    ApiHttpbinPost()\
        .set_json({"user_id":user_id})\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/post")\
        .validate("json().headers.Accept","application/json")\
        .validate("json().json.user_id","xyq18")

def test_httpbin_extract():
    api_run = ApiHttpbinGet().run()
    status_code = api_run.extract("status_code")
    assert status_code == 200

    server = api_run.extract("headers.server")
    assert server == "gunicorn/19.9.0"

    accpet_type =  api_run.extract("json().headers.Accept")
    assert accpet_type == "application/json"

def test_httpbin_setcookies():
    api_run = ApiHttpbinGetCookies()\
        .set_cookie("freeform1","123")\
        .set_cookie("freeform2","456")\
        .run()
    freeform1 = api_run.extract("json().cookies.freeform1")
    freeform2 = api_run.extract("json().cookies.freeform2")
    assert freeform1 == "123"
    assert freeform2 == "456"

def test_httpbin_parameters_extract():
    # get value
    freeform = ApiHttpbinGetCookies()\
        .set_cookie("freeform","123")\
        .run()\
        .extract("json().cookies.freeform")
    assert freeform == "123"

    # use value as parameter
    ApiHttpbinPost()\
        .set_json({"freeform":freeform})\
        .run()\
        .validate("status_code",200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url","https://httpbin.org/post")\
        .validate("json().headers.Accept","application/json")\
        .validate("json().json.freeform",freeform)
 
def test_httpbin_login_status():
    # login and get cookie
    ApiHttpbinSetCookies().set_params(freeform = "567").run()

    # request anther api, check cookie
    resp = ApiHttpbinPost()\
        .set_json({"abc":123})\
        .run()\
        .get_responce()
    request_headers = resp.request.headers
    assert "freeform=567" in request_headers["Cookie"]