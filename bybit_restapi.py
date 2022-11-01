import time
import hmac
import hashlib
import asyncio
import aiohttp

class bybitapi:
    def __init__(self):
        self.apikey = ""
        self.apisecret = ""
        self.bybit_endpoint_url = "https://api.bybit.com"
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())    #windowsの時はこれがないとeventlooperror
        return

    async def HTTP_Request(self, endpoint, method, payload):
        httpClient=aiohttp.ClientSession()
        recv_window=str(5000)
        time_stamp=str(int(time.time() * 10 ** 3))
        signature=self.genSignature(payload, time_stamp, recv_window)
        headers = {
            'X-BAPI-API-KEY': self.apikey,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'Content-Type': 'application/json'
        }
        async with httpClient as client:
            retryt = 10
            while retryt < 10240:
                try:
                    if(method=="POST"):
                        response = await client.request(method, self.bybit_endpoint_url + endpoint, headers=headers, data=payload)
                    else:
                        response = await client.request(method, self.bybit_endpoint_url + endpoint + "?" + payload, headers=headers)            

                    assert response.status == 200, f'status code error {response.status}'
                    response = await response.json()
                    print(response)
                    return
                except AssertionError as e:
                    print(e)
                    time.sleep(retryt)
                    retryt *= 2

    #署名生成
    def genSignature(self, payload, time_stamp, recv_window):
        param_str= str(time_stamp) + self.apikey + recv_window + payload
        hash = hmac.new(bytes(self.apisecret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
        signature = hash.hexdigest()
        return signature
    
    def test(self):
        #endpoint =  "/unified/v3/private/position/list"
        #method = "GET"
        #params = 'category=linear'
        
        endpoint = "/unified/v3/private/account/wallet/balance"
        method = "GET"
        params = ''
        
        asyncio.run(self.HTTP_Request(endpoint, method, params))
        return
    
    
if __name__ == "__main__":
    bb = bybitapi()
    bb.test()
