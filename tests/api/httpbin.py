from apitest.api import BaseApi

class ApiHttpbinGet(BaseApi):
    
    url = "https://httpbin.org/get"
    params = {}
    method = "GET"
    headers = {"Accept": "application/json"}


class ApiHttpbinPost(BaseApi):
    
    url = "https://httpbin.org/post"
    method = "POST"
    headers = {"Accept": "application/json"}
    json = {"xyq":18}