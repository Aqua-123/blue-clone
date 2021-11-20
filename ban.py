import requests
import threading 
import json 
import websocket

cookies = "MjExNjU0ODI%3D--dcb1a7de9cc8beb8b610514e3128d8ba1dd42f57"
acc_list = [
    "FT4l48XT9HFDwb3qChYARQ,MjExNjU0ODI%3D--dcb1a7de9cc8beb8b610514e3128d8ba1dd42f57",
    "ZzmTJ8_6-Qe8k1MvrXU6jQ,MjExNjQ3OTY%3D--204c364b996cb3f4a8d67889f15069c923222a1e",
    "ChpgGWx3HjKujbJLISOY4Q,MjExNjUwNTk%3D--3b70f09b95306fea769d15b40eb0fb791f8b6201",
    "SvN_I3Rp51rz5Y16A0QJhg,MjExNjUwODg%3D--5b1ad008c2d71aeb4a9cfb82f9ac2385795d0af2",
    "YxNT059JbSYIJ_VyYwcwtQ,MjExNjU0ODk%3D--641d9c14a37498fc286e8c35fa8a0f7bfe9322ab",
    "i5k_L2FonWp7HI-gncZuAA,MjExNjYzMTg%3D--4ea03ee8e559c04c60837bdd6015c5785eb06f24",
    "s54g0JSjOseUAqaSPl3EOg,MjExNjU2MzU%3D--1fd542f8fe5a0a196242dca59f83f4e3860a3993",
    "4ff_WgSHz6nOuiDlVJj39w,MjExNjU2Mzk%3D--2c3ec0eeaa007d736879c4f08badb0ea0349f611",
    "Oe4SET_Z_YOOjb6CY2NBjw,MjExNjYxMTU%3D--4837ebb82802084353f3f55a86f34fe6cc80b7a6",
    "Ey5s0A-nIAXJIFjvxkkwSA,MjExNjY5MDA%3D--c2ee4855d0ea473f9351fbf6206c4baadcdbc197",
    "FhtGe1lVKwxdwxUIvrOF7Q,MjExNjY2Mjc%3D--424b6821078de44f8bb8e6d070362f46b7f10bee",
    "bo8L4e3-XCbDTfVLqGXCng,MjExNjY5OTQ%3D--24af2140320cb82f4924309019b9af05f610b942",
    "BAb8fCzcmwGJ5QG1YG_hug,MjExNjczNTQ%3D--246b750c37acb02b1bed19e13649cd0fae17ba9c",
    "bc9N8HBVmrv1HVPj2D6tfA,MjExNjc0Nzk%3D--0118e3999c8d995a185c04cafc3b0264aa7c2647",
    "5Te_1wM9hPmVof6Asm5WUA,MjExNjc1NTU%3D--2e3e66b4d5b33a899eaaf3a69e031deaff6bbeec",
    "H3x4ZrTjR9tu6ESojPFCRA,MjExNjc4MTU%3D--ac3a05086f9b73079530cfc51c51618114c2ec62",
    "9lwNtZgNYBsOigWtSD6cXA,MjExNzMwODE%3D--0b11233b91b846547d64ef734d76c72c82e22b8a",
    "Og8Ar6Ao-VtDiwHsMpwpFg,MjExNzI1Mjk%3D--f4b2e73d600354bf406e307aaf01266919a91ca6",
    "69TSKMn4rjwoJNOSdCqpmw,MjExNzI1ODM%3D--ced3b24dab6c17f3d5414ceb14bb27b2dc4fb3d6",
    "2Zl3Z31RDpL7Hkv90Btldw,MjExNzI2MzY%3D--a53fb98aaa0e8d134d9ba2b74869568b3abd28e0",
    "783UwntXn0IYWf3Zh6-TcA,MjExNzMxNTc%3D--38ab99c194213ef4451dc8ca28516ea99facff60",
    "BQ1sJQPjltSw1d9ZZR3sUw,MjExNzMxMjA%3D--b3bfbb271ff31bdf896bfbbb40afb30accfe5eac",
    "cQd_MfLebikT67QTG9ISSg,MjExNzI5NzI%3D--6a91350eb7d3a5e41f36fc35b155a8ff6759c497",
    "Tm4sZRgvUTvX4XDmK4w8MA,MjExNzMxOTI%3D--1f80152383366ad1e0a6b91df577311069ca14f9",
    "qis5XYjo7YimxTCzda8Ibg,MjExNzMyNTU%3D--5bcb825ef48effe21f244c22316222a1ffd20fd5",
    "Dr5MIJDF1bEVpIYR0jyFuQ,MjExNzMyOTY%3D--27bbc78876bc1b79f14d9e8289a726c6cab0c6d2",
    "n3dv4s4yde5W2I9Q76zA5Q,MjExNzQ0OTI%3D--9f81929aa0ea829a8d85fa86b0923604967cfdc5",
    "p7iE1QTe8hiPUmiIayrTpA,MjExNzQ1NTk%3D--8852d4fb4074372653c53a0ab028a23926d097f1",
    "lctQi1hMOgDL9aqGwAzlNA,MjExNzQ2MDg%3D--a4763efe1b8631066fdee681d54eec7ba278ca9e",
    "i71AJNDiNTdtFHXQOAEzLg,MjExNzQ2NzQ%3D--fe819817818ddb23f509a6ef8aad48ecd0d59d7f",
    "tt2dyo2Qpezas2_M67JF7w,MjExNzQ3MTg%3D--861d6c27160e327cf79ebdf512e8ddb8d5f4634b",
    "GIE0iVrhyE-Tuk8WPcaehw,MjExNzQ5MjM%3D--31c2b058b7298c861962899cf4a9394053068619",
    "uov1svaa_q_CBA6yx_bS5Q,MjExNzUxODQ%3D--f903c2d1dfa3fe26805f11b4b6d2730dc5eff693",
    "FFXUElEpzBNxS3TjoF7DLA,MjExNzUyODc%3D--3df58e91c86b762677a68905a3f2ffe87c9d677e",
    "UryGCZtmJv0XafpiiOVjPg,MjExNzUzNDQ%3D--f4c5711f0ae4c107c62306e8907c28b5377c467a",
    "AxWd02MXJ-l4Xp60a6tbqQ,MjExNzUzODU%3D--1cfd14cde94ef52413f0e72e14c30f70cc7c77c8",
    "RRbCbhH35RpC-oT_DMYGNA,MjExNzU0MTc%3D--0625a18ed7be7a92b2f15aa0494e65510471ff42",
    "mqRz90NRaxYRgc1OZQ83-Q,MjExNzU0NTI%3D--15beaaba3086c47d196bfcff642ee4831e9607c4",
    "zTDF7v79s38OYaiNolQirg,MjExNzU1MDg%3D--f34ae2136eab504543511182fad40b25b56415df",
    "__W96sRY2v2jeJ47l9r11w,MjExNzU1NDk%3D--4afbbbe92569dccc636ce42d2e8f83aa19402bbd",
    "QNceOvfexIxmTPwGoYh_3w,MjExNzkzNDg%3D--b85625417d816473ae1317977b346433429b72f1",
    "cB6a_VuQxqBBwz0XrLXc5g,MjExNzkzODI%3D--d46d185d097413379b829b0e92386d8c8f58e9a5",
    "Gnwd16wVyl0ovSWGtpfYng,MjExNzk0MjI%3D--4f5f91b07243ebd6556e5d04d04c4b7dae285968",
    "c_MFptSEkZgAHtZa1j2m-w,MjExNzk0NDk%3D--427c7cdcca972719e5bd050f7dafae9e02faf1ae",
    "2yp6h1inuuN5XRz2a4u3Lg,MjExNzk0ODE%3D--f3a5f3467691993bf72f677257fe04940ab15a24",
    "JgkiCthzrEyHvaj1xXmpxQ,MjExNzk1MTE%3D--9fe66932a8e30665845e241f4255eb9ae58de68f",
    "84y6cx2taGOyIyPiNiG_Lw,MjExNzk3NjY%3D--3f2410bf6411db5e820c3cd3ff092ecfaecdfd21",
    "8rFYm1KOMPTqapG1q2NQwg,MjExNzk4NTc%3D--2d956c3f393f9dd3076dfb644622e1f3316a70ce",
    "uVMq7BlK2UBtuZp_lpibQA,MjExNzk4ODY%3D--9a49b6314b1e698de2e010f67dbbbb2eb4a30e14",
    "OZGhSCOmpvk-k1r_qUZnGg,MjExNzk5MTM%3D--1e28f44aa734e88ba33a01cb9916e795b745040d"
]
ban_list = ["Anthony"]
list_id =  ["48","56","33","39","38","40","34","51","58","57","41","54","37","53","43","42","49","55","59","44","46","36","60","52","32","50","47","35","45"]
a = 0 
websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("wss://www.emeraldchat.com/cable", cookie="user_id=MjExNzk5MTM%3D--1e28f44aa734e88ba33a01cb9916e795b745040d",subprotocols=["actioncable-v1-json", "actioncable-unsupported"],origin="https://www.emeraldchat.com",header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}, timeout = 1000000  )
def connect(n):
    connect_json= {"command":"subscribe","identifier":"{\"channel\":\"RoomChannel\",\"room_id\":\"channel"+ n+ "\"}"}
    ws.send(json.dumps(connect_json))
p = "-1"
def downvote(id,remem,user):
    req = requests.get("https://www.emeraldchat.com/karma_give?id="+str(id)+"&polarity="+p+"=HTTP/2", cookies={'remember_token': remem, 'user_id': user})
def thread(id,remem,user):
    processThread = threading.Thread(target=downvote, args=(id,remem,user))
    processThread.start()
    
def banfunc(id):
    for cook in acc_list:
        a = cook.split(",")
        user_id = a[0]
        remem = a[1]
        thread(id,remem,user)
for i in range (0,len(list_id)):
    n = list_id[i]
    connect(n)
action_list = ["user_connected","typing","user_disconnected","message"]
while True:
    print(ws.recv())
    server_reply = (ws.recv())
    print(server_reply)
    a = json.loads(server_reply)
    if ("identifier" in a.keys()) and ("message" in a.keys()) :
        b = a["message"]
        if  ("user" in b.keys()):
            for action in action_list:
                if (action in b.keys()) :
                    user = b["user"]
                    if "display_name" in user.keys():
                        name = user["display_name"]
                        if name in ban_list:
                            id = user["id"]
                            print("banning " + name + " " +str(id))
                            banfunc(id)
                else:
                    pass