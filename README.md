# awesome-python3-webapp
A python3 webapp demo

* [前期准备](#prepare)
* [ORM](#orm)
* [Web 框架](#web)
* [配置文件](#configutation)
* [MVC](#mvc)
* [构建前端](#template)
* [编写 API](#api)
* [Cookies](#cookies)
* [热更新](#hotUpdate)
* [部署 Web App](#deploy)

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

## <span id='web'>Web 框架</span>
* get 装饰器
* post 装饰器
* RequestHandler：从URL函数中分析其需要接收的参数，从request中获取必要的参数，调用URL函数，然后把结果转换为web.Response对象
* `add_route` 函数，用来注册一个URL处理函数
* 加入 `middleware`、`jinja2` 模板和自注册的支持

	> `middleware` 是一种拦截器，一个URL在被某个函数处理前，可以经过一系列的`middleware`的处理。

	> 一个`middleware`可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回。`middleware`的用处就在于把通用的功能从每个URL处理函数中拿出来，集中放到一个地方。

## <span id='configutation'>配置文件</span>
通常，一个Web App在运行时都需要读取配置文件，比如数据库的用户名、口令等，在不同的环境中运行时，Web App可以通过读取不同的配置文件来获得正确的配置。

* config_default
* config_override
* merge

## <span id='mvc'>MVC</span>

* `@get` `@post` 装饰器处理 URL
* `__template__`模板文件

## <span id='template'>构建前端</span>

* static 文件夹：资源文件
* `__base__.html`
* `block` 继承
* `jinja2`模板引擎，filter 过滤器
 
	```
	<p class="uk-article-meta">发表于{{ blog.create_at }}</p>
	```
	
## <span id='api'>编写 API</span>

* REST 风格
	
	> REST就是一种设计API的模式。最常用的数据格式是JSON。由于JSON能直接被JavaScript读取，所以，以JSON格式编写的REST风格的API具有简单、易读、易用的特点。
	
* 编写API的好处：由于API就是把Web App的功能全部封装了，所以，通过API操作数据，可以极大地把前端和后端的代码隔离，使得后端代码易于测试，前端代码编写更简单。

## <span id='cookies'>Cookies</span>

* 采用直接读取cookie的方式来验证用户登录，每次用户访问任意URL，都会对cookie进行验证，这种方式的好处是保证服务器处理任意的URL都是无状态的，可以扩展到多台服务器。

	> 由于HTTP协议是一种无状态协议，而服务器要跟踪用户状态，就只能通过cookie实现。大多数Web框架提供了Session功能来封装保存用户状态的cookie。
	> Session的优点是简单易用，可以直接从Session中取出用户登录信息。
	> Session的缺点是服务器需要在内存中维护一个映射表来存储用户登录信息，如果有两台以上服务器，就需要对Session做集群，因此，使用Session的Web App很难扩展。

* 防伪算法

	`"用户id" + "过期时间" + SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")`
	
	算法的关键在于SHA1是一种单向算法，即可以通过原始字符串计算出SHA1结果，但无法通过SHA1结果反推出原始字符串。
	
* cookie 的存取与解析
* 利用middle在处理URL之前，把cookie解析出来，并将登录用户绑定到 `request` 对象上，这样，后续的URL处理函数就可以直接拿到登录用户

## <span id='hotUpdate'>热更新</span>
* `watchdog` 利用操作系统的 API 监控目录文件的变化，并发送通知 

	```
	pip3 install watchdog
	```
* 利用 `watchdog` 接收文件变化的通知，如果是.py文件，就自动重启 `app.py` 进程。
* 利用 Python 自带的 `subprocess` 实现进程的启动和终止，并把输入输出重定向到当前进程的输入输出中。
* `./pymonitor.py app.py`


## <span id='deploy'>部署 Web App</span>

* 安装 [VirtualBox](https://www.virtualbox.org/) 虚拟机
* 选择 linux 的服务器版本 [Ubuntu Server 14.04 LTS](https://ubuntu.com/download/server)
* ssh 服务正常运行
	
	```
	 sudo apt-get install openssh-server
	```
	
* 用到的服务
	* Nginx：高性能Web服务器+负责反向代理
	* Supervisor：监控服务进程的工具
	* MySQL：数据库服务
* 安装服务

	```
	$ sudo apt-get install nginx supervisor python3 mysql-server
	```
	
	* [Ubuntu安装python 3. 7](https://www.jianshu.com/p/6059f7fc2cd0)

		```
		sudo ./configure --enable-optimizations --with-ssl
		sudo make install
		```
	*  `sudo apt-get install python3.7`
	* 安装 pip
	
		```
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python get-pip.py
		```
		`pip3` 在 /usr/local/目录下，不能直接执行 `pip3` 命令，so
		
		```
		sudo ln -s /usr/local/bin/pip3 /usr/bin/pip3
		```
		
	* 卸载 pip
	
		```
		sudo pip uinstall pip
		```
	
* 安装项目依赖库

	```
	sudo pip3 install jinja2 aiomysql aiohttp
	```
* 部署

	* 自动化部署：[Fabric](http://www.fabfile.org/)是一个自动化部署工具
	* 在本机安装 Fabric， Fabric 是用 Python2.x 开发的，本机需要支持 Python2.7 [Fabric安装](https://www.cnblogs.com/madsnotes/articles/5744814.html)
		
		```
		sudo pip2 install fabric
		```
		
		安装过程中出现的错误
		
		```
		NameError: name 'platform_system' is not defined
		```
		
		升级 pip 和 setuptools
		
		```
		pip intall --upgrade pip
		pip install --upgrade setuptools --user
		```
	* 编写脚本 `fabfile.py`

		```
		fab build
		```
		
* 复制文件到 Ubuntu
	* 设置-共享文件夹-新建挂载点 `UbuntuShare `
	* 在 Ubuntu /etc 目录下新建文件夹 `UbuntuShare`
	* `sudo mount -t vboxsf 挂载点名称(UbuntuShare) /etc/UbuntuShare`
	
		```
		mount: /mnt/UbuntuShare: wrong fs type, bad option, bad superblock on www, missing codepage or helper program, or other error.
		```
		
		[错误解决](https://my.oschina.net/jishuge/blog/2990051)

* ssh 连接
	
	* 查看 Ubuntu IP 地址
		
		```
		ifconfig
		```
	* 若 IP 地址以 10(10.0.2.15) 开头，修改网络连接方式

		设置 -> 网络 -> 网卡1 -> 连接方式 -> 修改为 桥接网卡
		
* 防火墙（服务器）

	```
	sudo ufw status  # 查看防火墙状态
	
	sudo ufw disable # 关闭防火墙
	
	sudo ufw enable  # 开启防火墙，并在系统启动时自动开启
	sudo ufw default deny # 关闭所有外部对本机的访问，但本机访问外部正常
	
	sudo ufw allow 80/tcp # 80 端口允许 tcp 访问
	sudo ufw allow 80/udp
	sudo ufw allow 80
	```
* 部署

	* deploy `fab deploy`
	
	* 在服务器主机创建软连接
		
		```
		pwd
		/etc/ngnix/sites-enabled
		sudo ln -s /etc/nginx/sites-available/awesome .
		```
	* 重加载 ngnix 服务
	
		```
		sudo /etc/init.d/ngnix reload
		```
		
		* 在 reload 之前需要删除 sites-enabled default 软连接，否则不能连接到 Web 项目
		* 需要通过 IP 地址访问	