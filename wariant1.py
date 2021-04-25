from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Callable
from collections import deque
from numbers import Number
from unittest import TestCase
import unittest

class Leaf:
    
    def __set_name__(self, owner: Node, name: str):
        self.private_name = '_' + name
    
    def __get__(self, obj: Node, objtype=None) -> Node:
        return getattr(obj, self.private_name, None) 
    
    def __set__(self, obj: Node, value: int):
        if not self.__get__(obj, type(obj)):
            new_node = Node(data=value, up=obj)
            setattr(obj, self.private_name, new_node)   
        else:
            getattr(obj, self.private_name).data = value
        

@dataclass
class Node:
    data: int
    left = Leaf()
    right = Leaf()
    up: Optional[Node] = None
    
    def __repr__(self):
        return f"Node(data={self.data})"
    
    def __str__(self):
        return self.__repr__()


class Tree:
    
    @staticmethod
    def dfs(node: Node) -> Node:
        stack = deque()
        while node or len(stack):
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield node
                node = node.right
                
    
    @staticmethod
    def __validate_node(node: Node):
        if not (node and isinstance(node, Node)):
            raise ValueError(f'node should be of type Node, not {type(node)}')

    
    @staticmethod
    def sum(node: Node) -> int:
        Tree.__validate_node(node)
        return sum(x.data for x in Tree.dfs(node))
    
    @staticmethod
    def mean(node: Node) -> Number:
        Tree.__validate_node(node)
        values = [x.data for x in Tree.dfs(node)]
        return sum(values) / len(values)
    
    @staticmethod
    def median(node: Node) -> Number:
        Tree.__validate_node(node)
        values = [x.data for x in Tree.dfs(node)]
        if len(values) < 2:
            raise ValueError('Not enough values to calculate a median')
        values = sorted(values)
        if len(values) % 2:
            return values[len(values)//2]
        else:
            return (values[len(values)//2 -1] + values[len(values)//2])/2


class TestNode(TestCase):
    
    def setUp(self):
        self.node = Node(data=7)
        
    def test_create(self):
        self.assertEqual(self.node.data, 7)
    
    def test_right_left(self):
        self.node.right = 1
        self.node.left = -1
        self.assertEqual(self.node.right, Node(data=1, up=self.node))
        self.assertEqual(self.node.left, Node(data=-1, up=self.node))
        self.assertEqual(self.node.right.up, self.node)
        self.assertEqual(self.node.left.up, self.node)
        self.assertEqual(self.node.right.data, 1)
        self.assertEqual(self.node.left.data, -1)
    
    def test_str(self):
        self.assertEqual(str(self.node), 'Node(data=7)')
    
class TestTreeMethods(TestCase):
    
    def setUp(self):
        root = Node(5)
        root.left = 3
        node = root.left
        node.left = 2
        node = node.left
        node = node.up
        node.right = 5
        node = node.right
        root.right = 7
        node = root.right
        node.left = 1
        node = node.left
        node = node.up
        node.right = 0
        node = node.right
        node.left = 2
        node = node.left
        node = node.up
        node.right = 8
        node = node.right
        node.right = 5
        node = node.right
        self.root = root
        
    def test_dfs(self):
        self.assertEqual(
            first=[
                2, 3, 5, 5, 1, 7, 2, 0, 8, 5 
            ],
            second=[x.data for x in Tree.dfs(self.root)]
        )
    
    def test_sum(self):
        self.assertEqual(
            first=38,
            second=Tree.sum(self.root)
        )
        self.assertEqual(
            first=10,
            second=Tree.sum(self.root.left)
        )
        self.assertEqual(
            first=23,
            second=Tree.sum(self.root.right)
        )
        self.assertEqual(
            first=2,
            second=Tree.sum(self.root.left.left)
        )
    
    def test_mean(self):
        self.assertEqual(
            first=3.8,
            second=Tree.mean(self.root)
        )
        self.assertEqual(
            first=(10/3),
            second=Tree.mean(self.root.left)
        )
        self.assertEqual(
            first=(23/6),
            second=Tree.mean(self.root.right)
        )
        self.assertEqual(
            first=2,
            second=Tree.mean(self.root.left.left)
        )
        
    def test_median(self):
        self.assertEqual(
            first=4,
            second=Tree.median(self.root)
        )
        self.assertEqual(
            first=3,
            second=Tree.median(self.root.left)
        )
        self.assertEqual(
            first=3.5,
            second=Tree.median(self.root.right)
        )
        with self.assertRaises(ValueError):
            Tree.median(self.root.left.left)
            
            
if __name__ == '__main__':
    unittest.main()