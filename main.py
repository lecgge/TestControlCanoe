import json
import time
import asyncio
from pickle import GLOBAL

import requests
from py_canoe import CANoe
from py_canoe_utils.app_utils.configuration import testReport, getReportPath, TestEnvironment
import websockets


def runCanoe(project):
    global UDS_PATH, FBL_PATH, GALAXY_PATH
    path = ""
    i = -1
    print("start case")
    match project:
        case "UDS":
            path,i = _runCanoe(UDS_PATH,"UDSonCAN_ADC")
        case "FBL":
            path,i = _runCanoe(FBL_PATH,"FBL")
        case "Galaxy":
            path,i = _runCanoe(GALAXY_PATH,"HardTest")
    return path,i


def _runCanoe(projectPath,testModule):
    canoe_inst = CANoe(py_canoe_log_dir=fr'.\py_canoe\py_canoe_log')
    canoe_inst.open(canoe_cfg=projectPath, visible=True, auto_save=False,
                    prompt_user=False)

    canoe_inst.start_measurement()
    time.sleep(1)

    # env :TestEnvironment= canoe_inst.get_test_environments().get("HardTest")
    # env.Items
    # testmodule = canoe_inst.get_test_modules("HardTest")
    # hardtest = testmodule.get("HardTest")
    #
    # print(canoe_inst.get_test_modules("HardTest"))

    i: int = canoe_inst.execute_test_module(testModule)
    print(i)

    time.sleep(1)
    canoe_inst.stop_measurement()
    canoe_inst.quit()
    print(getReportPath())
    return getReportPath(), i

def send_file(filepath):
    # 定义接口 URL
    url = "http://192.168.192.50:8100/tmp/api/savefile/save"

    # filepath.replace("\\","\\\\")
    # 定义要上传的文件
    files = {'file': open(filepath, 'rb')}

    # 定义请求头（如果需要）
    headers = {
        'Authorization': 'Bearer your_token_here'  # 如果需要认证
    }

    # 发送 POST 请求
    response = requests.post(url, files=files)

    # 检查响应状态码
    if response.status_code == 200:
        print("File uploaded successfully!")
        print("Response:", response.json())  # 假设返回的是 JSON 格式
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print("Response:", response.text)
    data = json.loads(response.text)
    result = data.get('result')
    return result
async def main():
    uri = f"ws://192.168.192.50:8100/tmp/testwebsocket/e9ca23d68d884d4ebb19d07889727dae/{deviceId}"
    # path = r"D:\GalaxyTest\GalaxyTest\TestReport&Log\2024_10_30_15_24_34\__HardTest_2024_10_30_15_24_34.html"
    # path.replace("\\","\\\\")
    # send_file(path)
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                print("in")
                # 接收消息
                response = await websocket.recv()
                print(f"Received: {response}")
                request = response.split(":")
                if len(request) == 2 and request[1] == "Start":
                    filepath, result = runCanoe(request[0])
                    filepath.replace("\\", "\\\\")
                    result1 = send_file(filepath)
                    # 发送消息
                    await websocket.send(result1)


        except websockets.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



if __name__ == '__main__':
    with open('params.json', 'r') as file:
        data = json.load(file)
        UDS_PATH = data["UDS_PATH"]
        FBL_PATH = data["FBL_PATH"]
        GALAXY_PATH = data["GALAXY_PATH"]
        deviceId = data["deviceId"]
        print(UDS_PATH)
        print(FBL_PATH)
        print(GALAXY_PATH)
    # runCanoe()
    asyncio.run(main())

