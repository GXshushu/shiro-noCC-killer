这是一个shiro550反序列化漏洞的利用工具，只有shiro自身链，能够攻击没有使用cc链的目标，能够探测commons beautils的版本和加解密模式，并根据版本和加密模式来达成命令执行。暂时只有TomcatEcho回显方式

运行要求，有java环境，java也在环境变量中

需要自己提供密钥，没有密钥爆破功能

命令行启动程序
```
python main.py --url http://target/ --key shiro-key
```
运行实例
![image](https://github.com/GXshushu/shiro-noCC-killer/assets/73958525/16df1b5b-02a8-4ade-a91b-8365462dbe60)

![image](https://github.com/GXshushu/shiro-noCC-killer/assets/73958525/63244d98-db98-4a81-936f-4c75eb79bc3a)
![image](https://github.com/GXshushu/shiro-noCC-killer/assets/73958525/c8faf7ee-347a-4676-870b-50d6e1ae60ae)
