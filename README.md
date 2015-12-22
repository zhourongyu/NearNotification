# NearNotification

Python 打包的一款简陋的 OSX App，通过 OSX 的 Notiication 来提醒（含下单）「好近」的特价信息，

## 环境及依赖：
	
* OSX EI Capitan
* Python 2.7
* pyobjc 3.0.4
* py2app 0.9
	

## 备注：

 - 每 30 秒查询一次没结束的活动中价格低于 2 元且还有库存的优惠信息
 - 缺陷有很多，例如启动后只能右键强制退出；无限重复通知等
 - 监听价格及轮询间隔只能改代码后重新打包~
 - 暂时没有模拟登陆，如果想使用下单，自行从 App 中抓取出自己的 session_id 及 sid，通过命令行方式启动 ./NearNotification session_id sid
 	
 


