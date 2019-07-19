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