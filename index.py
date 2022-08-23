#utf-8
#pip install websockets
#引入库 asyncio-线程异步 websockets-通讯协议 ssl-证书 gzip-压缩文件
import asyncio,websockets,ssl,gzip
user={}
room={}
async def inputentrance(websocket):
    global data
    while True:
        try:
            recv_str = await websocket.recv()
            recv_str=gzip.decompress(recv_str).decode()
            if str(websocket.path) == '/0':
                response_str = str(recv_str)+' 加入成功'
            else:
                response_str = str(recv_str)+' Join successfully'

            response_str = gzip.compress(response_str.encode("utf-8"))
            await websocket.send(response_str)
            try:
                try:
                    for i in user:
                        if user[i] in room[recv_str]:
                            if str(i.path) == '/0':
                                response_str = str(user[websocket])[0:5] + ' 号用户加入了该房间' + recv_str
                            else:
                                response_str =  'User '+str(str(recv_str))[0:5]+' joined the room'+ recv_str
                            response_str=gzip.compress(response_str.encode("utf-8"))
                            await i.send(response_str)
                except:
                    if str(websocket.path) == '/0':
                        response_str = "你是本房间第一人 邀请小伙伴加入吧"
                    else:
                        response_str = 'You are the first person in this room, invite friends to join'
                    response_str=gzip.compress(response_str.encode("utf-8"))
                    await websocket.send(response_str)
                try:
                    recv_str=str(recv_str)
                    room[recv_str].append(user[websocket])
                except:
                    room[recv_str] = []
                    room[recv_str].append(user[websocket])
                return recv_str
            except:
                del user[websocket]
        except websockets.ConnectionClosedOK:
            try:del user[websocket]
            except:pass
            break
async def msghandle(websocket,entrance):
    while True:
        recv_str = await websocket.recv()
        try:
            for i in user:
                if user[i] in room[entrance]:
                    try:recv_str = gzip.decompress(recv_str).decode()
                    except:pass
                    try:
                        response_str=str(user[websocket])[0:5] + ': ' + recv_str
                        response_str = gzip.compress(response_str.encode("utf-8"))
                        await i.send(response_str)
                    except:pass
        except websockets.ConnectionClosedOK:
            try:del user[websocket]
            except:pass
            break
async def Mainthread(websocket):
    try:
        remote_ip = websocket.remote_address
        print('用户进入',remote_ip,websocket.id)
        user[websocket]=websocket.id
        if str(websocket.path) =='/0':
            response_str = '输入房间号就可以聊天啦'
        else:
            response_str = 'Enter the room number to chat'
        response_str = gzip.compress(response_str.encode("utf-8"))
        await websocket.send(response_str)
        entrance=await inputentrance(websocket)
        await msghandle(websocket,entrance)
    except websockets.ConnectionClosedOK:
        print('用户断开', websocket.id)
        try:
            for i in room:
                if user[websocket] in room[i]:
                    room[i].remove(user[websocket])
                    for o in user:
                        if user[o] in room[i]:
                            try:
                                if str(o.path) == '/0':
                                    response_str =str(user[websocket])[0:5] + ' 号用户离开了该房间'
                                else:
                                    response_str = 'User '+str(user[websocket])[0:5]+' left the room'
                                response_str = gzip.compress(response_str.encode("utf-8"))
                                await o.send(response_str)
                            except:print('离开报错')
        except: pass
        try:
            del user[websocket]
        except:pass
if __name__ == '__main__':
    #如需开启wss 可不需要注释 但需要自己创建pem
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain(r'localhost.pem')
    # start_server = websockets.serve(Mainthread, '0.0.0.0', 444,ssl=ssl_context)

    # 取消上面注释 下面这行要注释掉
    start_server = websockets.serve(Mainthread, '0.0.0.0', 444)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
