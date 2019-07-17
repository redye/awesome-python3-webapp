# awesome-python3-webapp
A python3 webapp demo

* [前期准备](#prepare)
* [ORM](#orm)


## <span id='prepare'>前期准备</span>
* python3
* 异步框架 `pip3 install aiohttp`
* 前端模板引擎 `pip3 install jinja2`
* MySQL 的 python 异步驱动程序 `pip3 install aiomysql `
* 项目结构
	
	```
	awesome-python3-webapp/  <-- 根目录
	|
	+- backup/               <-- 备份目录
	|
	+- conf/                 <-- 配置文件
	|
	+- dist/                 <-- 打包目录
	|
	+- www/                  <-- Web目录，存放.py文件
	|  |
	|  +- static/            <-- 存放静态文件
	|  |
	|  +- templates/         <-- 存放模板文件
	|
	+- ios/                  <-- 存放iOS App工程
	|
	+- LICENSE               <-- 代码LICENSE
	```
	
## <span id='orm'>ORM</span>
* 创建连接池
* 销毁连接池
* select 语句
* execute: insert、update、delete 语句
* Model 与 Metaclass
