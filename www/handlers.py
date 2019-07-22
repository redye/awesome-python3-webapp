#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers'

import re, time, json, logging, hashlib, base64, asyncio

import markdown2

from coroweb import get, post

from models import User, Comment, Blog, next_id

from apis import APIValueError, APIError, APIPermissionError, APIResourceNotFoundError, Page

from aiohttp import web

from config import configs

COOKIE_NAME = 'awesession'
__COOKIE_KEY = configs.session.secret
COOKIE_MAX_AGE = 86400
COOKIE_SIGN_OUT = '-deleted-'

def check_admin(request):
	if request.__user__ is None or not request.__user__.admin:
		raise APIPermissionError()

def get_page_index(page_str):
	p = 1
	try:
		p = int(page_str)
	except Exception as e:
		pass
	if p < 1:
		p = 1
	return p

def text2html(text):
	lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt').replace('>', '&gt'), filter(lambda s: s.strip() != '', text.split('\n')))
	return ''.join(lines)

def user2cookie(user, max_age):
	expires = str(int(time.time() + max_age))
	s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, __COOKIE_KEY)
	L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(L)


async def cookie2user(cookie_str):
	logging.info('cookie_str: %s' % cookie_str)
	if not cookie_str:
		return None
	if cookie_str == COOKIE_SIGN_OUT:
		return None

	try:
		L = cookie_str.split('-')
		if len(L) != 3:
			return None
		uid, expires, sha1 = L
		if int(expires) < time.time():
			return None
		user = await User.find(uid)
		if user is None:
			return None
		s = '%s-%s-%s-%s' % (uid, user.passwd, expires, __COOKIE_KEY)

		if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
			logging.info('invalid sha1')
			return None
		user.passwd = '******'
		return user
	except Exception as e:
		logging.exception(e)
		return None


# 首页
@get('/')
async def index(request):
	blogs = await Blog.findAll()
	count = len(blogs)
	if count <= 0:
		blogs = []
	return {
		'__template__': 'blogs.html',
		'blogs': blogs
	}

# 注册
@get('/register')
def regiseter(request): 
	return {
		'__template__': 'register.html'
	}

# 登录
@get('/signin')
def signin(request): 
	return {
		'__template__': 'signin.html'
	}

# 登出
@get('/signout')
def signout(request): 
	referer = request.headers.get('Referer')
	r = web.HTTPFound(referer or '/')
	r.set_cookie(COOKIE_NAME, COOKIE_SIGN_OUT, max_age=COOKIE_MAX_AGE, httponly=True)
	logging.info('user signed out.')
	return r


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

# 注册用户
@post('/api/users')
async def api_regiester_user(*, email, name, passwd):
	if not name or not name.strip():
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not passwd or not _RE_SHA1.match(passwd):
		raise APIValueError('passwd')
	users = await User.findAll('email=?', [email])
	if len(users) > 0:
		raise APIError('register:failed', 'email', 'Email is already in use.')
	uid = next_id()
	sha1_passwd = '%s:%s' % (uid, passwd)
	user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
	await user.save()
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, COOKIE_MAX_AGE), max_age=COOKIE_MAX_AGE, httponly=True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r

# 登录用户
@post('/api/authenticate')
async def authenticate(*, email, passwd):
	if not email:
		raise APIValueError('email', 'Invalid email.')
	if not passwd:
		raise APIValueError('passwd', 'Invalid password.')
	users = await User.findAll('email=?', [email])
	if len(users) == 0:
		raise APIValueError('email', 'Email not exist.')

	user = users[0]
	sha1 = hashlib.sha1()
	sha1.update(user.id.encode('utf-8'))
	sha1.update(b':')
	sha1.update(passwd.encode('utf-8'))
	if user.passwd != sha1.hexdigest():
		raise APIValueError('passwd', 'Invalid password.')
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, COOKIE_MAX_AGE), max_age=COOKIE_MAX_AGE, httponly=True)
	user.passwd = '******'
	r.content_type= 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r

# 日志创建
@get('/manage/blogs/create')
def manage_create_blog():
	return {
		'__template__': 'manage_blog.edit.html',
		'id': '',
		'action': '/api/blogs'
	}

@get('/manage/blogs/edit')
def manager_edit_blog(*, id):
	return {
		'__template__': 'manage_blog.edit.html',
		'id': id,
		'action': '/api/blogs/%s' % id
	}

@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
	check_admin(request)
	if not name or not name.strip():
		raise APIValueError('name', 'name cannot be empty')
	if not summary or not summary.strip():
		raise APIValueError('summary', 'summary cannot be empty')
	if not content or not content.strip():
		raise APIValueError('content', 'content cannot be empty')

	user = request.__user__
	blog = Blog(user_id=user.id, 
				user_name=user.name, 
				user_image=user.image, 
				name=name.strip(), 
				summary=summary.strip(),
				content=content.strip())
	await blog.save()
	return blog

@post('/api/blogs/{id}')
async def api_edit_blog(request, *, id, name, summary, content):
	check_admin(request)
	if not name or not name.strip():
		raise APIValueError('name', 'name cannot be empty')
	if not summary or not summary.strip():
		raise APIValueError('summary', 'summary cannot be empty')
	if not content or not content.strip():
		raise APIValueError('content', 'content cannot be empty')

	blog = await Blog.find(id)
	blog.name = name.strip()
	blog.summary = summary.strip()
	blog.content = content.strip()
	await blog.update()
	return blog



# 日志详情
@get('/api/blogs/{id}')
async def api_get_blog(*, id):
	blog = await Blog.find(id)
	return blog


@get('/blog/{id}')
async def get_blog(id):
	blog = await Blog.find(id)
	comments = await Comment.findAll('blog_id=?', [id], orderBy='create_at desc')
	for c in comments:
		c.html_content = text2html(c.content)
	blog.html_content = markdown2.markdown(blog.content)

	return {
		'__template__': 'blog.html',
		'blog': blog,
		'comments': comments
	}

@post('/api/blogs/{id}/delete')
async def api_delete_blog(*, request, id):
	check_admin(request)
	blog = await Blog.find(id)
	await blog.remove()
	return dict(id=id)

@get('/api/blogs')
async def api_blogs(*, page='1'):
	page_index = get_page_index(page)
	num = await Blog.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, blogs=())
	blogs = await Blog.findAll(orderBy='create_at desc', limit=(p.offset, p.limit))
	return dict(page=p, blogs=blogs)

@get('/manage/blogs')
def manager_blogs(*, page='1'):
	return {
		'__template__': 'manage_blogs.html',
		'page_index': get_page_index(page)
	}

@post('/api/comments/{id}/delete')
async def api_delete_comment(*, request, id):
	check_admin(request)
	comment = await Comment.find(id)
	await comment.remove()
	return dict(id=id)

@get('/api/comments')
async def api_comments(*, page='1'):
	page_index = get_page_index(page)
	num = await Comment.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, comments=())
	comments = await Comment.findAll(orderBy='create_at desc', limit=(p.offset, p.limit))
	return dict(page=p, comments=comments)

@get('/manage/comments')
def manager_comments(*, page='1'):
	return {
		'__template__': 'manage_comments.html',
		'page_index': get_page_index(page)
	}

@post('/api/blogs/{blog_id}/comments')
async def api_create_comment(*, blog_id, request, content):
	user = request.__user__
	if user is None:
		raise APIPermissionError('Please signin first')
	if not content or not content.strip():
		raise APIValueError('content', 'content cannot be empty')

	blog = await Blog.find(blog_id)
	if blog is None:
		raise APIResourceNotFoundError('Blog')
	comment = Comment(blog_id=blog.id, 
					  user_id=user.id, 
					  user_name=user.name, 
					  user_image=user.image,
					  content=content.strip())
	await comment.save()
	return comment

@get('/api/users')
async def api_users(*, page='1'):
	page_index = get_page_index(page)
	num = await User.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, users=())
	users = await User.findAll(orderBy='create_at desc', limit=(p.offset, p.limit))
	for u in users:
		u.passwd = '******'
	return dict(page=p, users=users)

@get('/manage/users')
def manage_users(*, page='1'):
	return {
		'__template__': 'manage_users.html',
		'page_index': get_page_index(page)
	}

