#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import orm

from models import User, Blog, Comment

import asyncio

import random


async def test(loop):
	
	await orm.create_pool(loop, user='www-data', password='www-data', database='awesome')

	u = User(id='001563346612358edaf8361163d4a7b8519752ad4eeb3e8000')

	# await u.save()
	# await u.remove()

	users = await User.findAll()
	for u in users:
		print('user => ', u)

	await orm.destroy_pool()

	
loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
print('test finished')
loop.close()