#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import orm

from models import User, Blog, Comment

import asyncio

import random


async def test(loop):
	
	await orm.create_pool(loop, user='www-data', password='www-data', database='awesome')

	u = User(id='00156334720523413f5dfc88a1343efb1a607f1a4a674d0000')

	# await u.save()
	await u.remove()

	await orm.destroy_pool()

	
loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
print('test finished')
loop.close()