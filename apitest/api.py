import requests

session = requests.sessions.Session()

class BaseApi(object):

    method = "get"
    url = ""
    params = {}
    headers = {}
    cookies = {}
    data = {}
    json = {}

    def __init__(self):
        self.responce = None

    def set_params(self,**params):
        self.params = params
        return self
    
    def set_cookie(self,key,value): 
        self.cookies.update({key:value})
        return self
    
    def set_data(self,data):
        self.data = data
        return self

    def set_json(self,json_data):
        self.json = json_data
        return self

    def run(self):
        self.responce = session.request(
            self.method,
            self.url,
            params=self.params,
            cookies = self.cookies,
            headers=self.headers,
            data=self.data,
            json=self.json)
        return self

    def extract(self,field):
        value = self.responce
        for _key in field.split("."):
            if isinstance(value,requests.Response):
                if _key == "json()":
                    value = self.responce.json()
                else:
                    value = getattr(value,_key)
            elif isinstance(value,(requests.structures.CaseInsensitiveDict,dict)):
                value = value[_key]

        return value

    def validate(self,key,except_value):
        # value = self.responce
        # for _key in key.split("."):
        #     if isinstance(value,requests.Response):
        #         if _key == "json()":
        #             value = self.responce.json()
        #         else:
        #             value = getattr(value,_key)
        #     elif isinstance(value,(requests.structures.CaseInsensitiveDict,dict)):
        #         value = value[_key]
        
        actual_value =self.extract(key)
        assert actual_value == except_value
        return self 

    def get_responce(self):
        return self.responce  
    
