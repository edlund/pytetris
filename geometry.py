#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import json
import random

def _swap(l, i, j):
	# Helper to make list swaps less verbose.
	l[i], l[j] = l[j], l[i]

def score(clrs):
	mult = len(clrs)
	base = 1000
	points = mult * base
	return (
		points,
		"{0}x line clear".format(mult)
	)

def drop(grid, clrs):
	# Drop blocks after a %clear()-call.
	for y0 in clrs:
		for y in xrange(y0, 1, -1):
			for x in xrange(0, grid.w):
				_swap(
					grid.cells,
					grid.coord_to_index(x, y - 0),
					grid.coord_to_index(x, y - 1),
				)

def clear(grid):
	# Detect and clear lines on the x-plane in the given grid.
	clrs = []
	width = grid.w
	height = grid.h
	
	for y in xrange(0, height):
		blks = []
		for x in xrange(0, width):
			b = grid.coord_to_block(x, y)
			if b.filled():
				blks.append(b)
		if len(blks) == width:
			if y:
				clrs.append(y)
			for b in blks:
				b.clear()
	return clrs

class Block:
	
	HOLLOW = 0
	FILLED = 1
	
	def clear(self):
		self.uid = 0
		self.value = 0
		self.color = '#000000'
		self.state = Block.HOLLOW
	
	def filled(self):
		return self.state == Block.FILLED
	
	def __init__(self, value, color, state):
		self.uid = 0
		self.value = value
		self.color = color
		self.state = state

class Grid:
	
	def coord_to_index(self, x, y):
		if x >= self.w or y >= self.h:
			raise IndexError()
		return self.w * y + x
	
	def coord_to_block(self, x, y):
		return self.cells[self.coord_to_index(x, y)]
	
	def assign_uid(self, uid):
		for b in self.cells:
			if b.state == Block.FILLED:
				b.uid = uid
	
	def assign_cells(self, blocks, color):
		for i in xrange(0, len(blocks)):
			if blocks[i]:
				self.cells[i] = Block(blocks[i], color, Block.FILLED)
	
	def list_cells(self):
		return [b.value for b in self.cells]
	
	def compare_cells(self, blocks):
		if len(self.cells) != len(blocks):
			return False
		for i in xrange(0, len(blocks)):
			if self.cells[i].value != blocks[i]:
				return False
		return True
	
	def print_cells(self):
		blocks = []
		for c in self.cells:
			blocks.append(c.value)
		chunkify = lambda L, n: [L[i : i + n] for i in range(0, len(L), n)]
		for chunk in chunkify(blocks, self.w):
			for b in chunk:
				print(" {0}".format(b), end="")
			print("")
	
	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.cells = [Block(0, str("#000000"), Block.HOLLOW)
			for _ in xrange(w * h)]

class Shape:
	
	R_000 = 0
	R_090 = 1
	R_180 = 2
	R_270 = 3
	
	@staticmethod
	def _rcw90(m, s):
		# Rotate the given "matrix" %m with side %s 90 degrees
		# clock-wise.
		if s == 2:
			_swap(m, 0, 3);
			_swap(m, 1, 3);
			_swap(m, 0, 2);
		else:
			a = s * s
			for y in xrange(0, s):
				for x in xrange(0, s - y):
					_swap(
						m,
						y * s + x,
						a - (x * s + y) - 1
					)
			# Every column is now reversed from top to bottom
			# and must be reversed to form the desired result.
			for x in xrange(0, s):
				for y in xrange(0, int(s / 2)):
					_swap(
						m,
						s * y + x,
						a - (s * y + (s - x - 1)) - 1
					)
		return m
	
	def assign_uid(self, uid):
		self.uid = uid
		for g in self.grids:
			g.assign_uid(uid)
	
	def rotation(self, index):
		return self.grids[index]
	
	def random_rotation(self):
		self.rindex = random.randint(0, 3)
	
	def rotate_cw(self):
		if self.rindex + 1 == len(self.grids): self.rindex = 0
		else: self.rindex += 1
	
	def rotate_ccw(self):
		if self.rindex == 0: self.rindex = len(self.grids) - 1
		else: self.rindex -= 1
	
	def grid(self):
		return self.grids[self.rindex]
	
	def __init__(self, desc):
		self.x = 0
		self.y = 0
		self.uid = 0
		self.desc = desc
		self.side = desc['side']
		self.grids = [Grid(self.side, self.side)
			for _ in xrange(0, 4)]
		for g in self.grids:
			g.assign_cells(Shape._rcw90(desc['blocks'],
				self.side), str(desc['color']))
		self.rindex = 0

class Factory:
	
	def __init__(self, path):
		self.nextuid = 0
		self.path = path
		self.shapes = []
		with open(path, 'r') as f:
			self.config = json.loads(f.read())
			self.width = self.config['width']
			self.height = self.config['height']
			self.block_size = self.config['block_size']
			for desc in self.config['shapes']:
				self.shapes.append(Shape(desc))
	
	def find(self, name):
		return next(s for s in self.shapes if s.desc['name'] == name)
	
	def spawn(self, w=0):
		self.nextuid += 1
		s = copy.deepcopy(random.choice(self.shapes))
		s.assign_uid(self.nextuid)
		s.random_rotation()
		if w > s.side:
			s.x = random.randint(0, w - 1 - s.side)
		return s

if __name__ == '__main__':
	import unittest
	
	class TestUtils(unittest.TestCase):
		
		def test__swap(self):
			l = ["world", " ", "hello", "!"]
			i = 0
			j = 2
			_swap(l, i, j)
			self.assertEqual("".join(l), "hello world!")
		
		def test_score(self):
			clrs = [6, 7, 8, 9]
			pts, msg = score(clrs)
			self.assertEqual(pts, 4000)
			self.assertEqual(msg, "4x line clear")
		
		def test_drop(self):
			w = 8
			h = 10
			clrs = [3, 6, 7, 8]
			playfield = [
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 1, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				1, 1, 1, 1, 0, 1, 1, 1,
				0, 1, 0, 0, 1, 1, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 1, 0, 1, 1, 0, 1, 1
			]
			expected = [
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 1, 0, 0,
				1, 1, 1, 1, 0, 1, 1, 1,
				0, 1, 0, 0, 1, 1, 0, 0,
				0, 1, 0, 1, 1, 0, 1, 1
			]
			
			gr = Grid(w, h)
			gr.assign_cells(playfield, '#f0f0f0')
			drop(gr, clrs)
			
			self.assertEquals(gr.list_cells(), expected)
		
		def test_clear(self):
			w = 8
			h = 10
			playfield = [
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 1, 0, 0,
				1, 1, 1, 1, 1, 1, 1, 1, # full
				1, 1, 1, 1, 0, 1, 1, 1,
				0, 1, 0, 0, 1, 1, 0, 0,
				1, 1, 1, 1, 1, 1, 1, 1, # full
				1, 1, 1, 1, 1, 1, 1, 1, # full
				1, 1, 1, 1, 1, 1, 1, 1, # full
				0, 1, 0, 1, 1, 0, 1, 1
			]
			expected = [
				0, 0, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 0, 0, 0,
				0, 1, 0, 0, 0, 1, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				1, 1, 1, 1, 0, 1, 1, 1,
				0, 1, 0, 0, 1, 1, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 0, 0, 0, 0, 0, 0, 0, # cleared
				0, 1, 0, 1, 1, 0, 1, 1
			]
			
			gr = Grid(w, h)
			gr.assign_cells(playfield, '#f0f0f0')
			clrs = clear(gr)
			
			self.assertEquals(gr.list_cells(), expected)
			self.assertEquals(clrs, [3, 6, 7, 8])
	
	class TestShape(unittest.TestCase):
		
		def test__rcw90(self):
			f = Factory("./tetrominos.json")
			
			Z = f.find('Z')
			self.assertTrue(Z.rotation(Shape.R_000).compare_cells([
				0, 0, 1,
				0, 1, 1,
				0, 1, 0
			]))
			self.assertTrue(Z.rotation(Shape.R_090).compare_cells([
				0, 0, 0,
				1, 1, 0,
				0, 1, 1
			]))
			self.assertTrue(Z.rotation(Shape.R_180).compare_cells([
				0, 1, 0,
				1, 1, 0,
				1, 0, 0
			]))
			self.assertTrue(Z.rotation(Shape.R_270).compare_cells([
				1, 1, 0,
				0, 1, 1,
				0, 0, 0
			]))
			
			Z = f.find('I')
			self.assertTrue(Z.rotation(Shape.R_000).compare_cells([
				0, 0, 0, 0,
				1, 1, 1, 1,
				0, 0, 0, 0,
				0, 0, 0, 0
			]))
			
			Z = f.find('O')
			self.assertTrue(Z.rotation(Shape.R_180).compare_cells([
				1, 1,
				1, 1,
			]))
		
		def test_rotate(self):
			f = Factory("./tetrominos.json")
			Z = f.find('Z')
			
			Z.rotate_cw()
			self.assertTrue(Z.grid().compare_cells([
				0, 0, 0,
				1, 1, 0,
				0, 1, 1
			]))
			
			Z.rotate_cw()
			self.assertTrue(Z.grid().compare_cells([
				0, 1, 0,
				1, 1, 0,
				1, 0, 0
			]))
			
			Z.rotate_ccw()
			self.assertTrue(Z.grid().compare_cells([
				0, 0, 0,
				1, 1, 0,
				0, 1, 1
			]))
	
	class TestFactory(unittest.TestCase):
		
		def test_find(self):
			f = Factory("./tetrominos.json")
			Z = f.find('Z')
			T = f.find('T')
			I = f.find('I')
			O = f.find('O')
			
			with self.assertRaises(StopIteration):
				Q = f.find('Q')
		
		def test_spawn(self):
			w = 10
			f = Factory("./tetrominos.json")
			s = f.spawn(w)
			self.assertEqual(s.uid, 1)
			self.assertTrue(s.x >= 0 and s.x < w - s.side)
			self.assertTrue(s.rindex >= 0 and s.rindex < len(s.grids))
	
	unittest.main()
	
	exit(0)

