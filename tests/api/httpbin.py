from apitest.api import BaseApi

class ApiHttpbinGet(BaseApi):
    
    url = "https://httpbin.org/get"
    method = "GET"
    params = {}
    headers = {"Accept": "application/json"}

class ApiHttpbinPost(BaseApi):
    
    url = "https://httpbin.org/post"
    
    method = "POST"
    headers = {"Accept": "application/json"}
    json = {"xyq":18}

class ApiHttpbinGetCookies(BaseApi):
    
    url = "https://httpbin.org/cookies"
    method = "GET"
    headers = {"Accept": "application/json"}
   