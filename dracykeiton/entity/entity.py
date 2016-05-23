##
##  Copyright (C) 2015 caryoscelus
##
##  This file is part of Dracykeiton
##  https://github.com/caryoscelus/dracykeiton
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##  
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

"""Contains Entity which is the base class for all entities and it's properties
"""
import functools
import collections
from six import add_metaclass

from ..compat import *
from ..util.priorityqueue import PriorityQueue
from ..util.dependency import DependencyTree
from ..util import curry

class DynamicProperty(object):
    """Stores dynamic property and modifiers associated with it."""
    def __init__(self, owner, empty=None, priorities=(), default=None):
        self.getters = PriorityQueue(*priorities, default=default)
        self.setters = PriorityQueue(*priorities, default=default)
        self._value = empty
        self.owner = owner
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return '<DynamicProperty {}>'.format(repr(self.value))
    
    def __getstate__(self):
        # we expect somebody else to add all the nodes since we can't
        # store them from here
        if self.getters or self.setters:
            self_copy = DynamicProperty(self.owner, self._value, priorities=self.getters.priorities, default=self.getters.default)
            return self_copy.__getstate__()
        return self.__dict__
    
    @property
    def value(self):
        value = self._value
        for mod in self.getters:
            value = mod(self.owner, value)
        return value
    
    @value.setter
    def value(self, value):
        for mod in self.setters:
            value = mod(self.owner, value)
        self._value = value
    
    def add_set_node(self, f, priority=None):
        self.setters.add(f, priority)
    
    def add_get_node(self, f, priority=None):
        self.getters.add(f, priority)
    
    def del_set_node(self, f):
        self.setters.remove(f)
    
    def del_get_node(self, f):
        self.getters.remove(f)

class EntityMeta(type):
    def __init__(self, name, bases, d):
        type.__init__(self, name, bases, d)
        self._global_mods = list()
        self._mod_deps = list()

def get_mods_deps(cl):
    return cl._mod_deps

def mod_dep(*mods):
    """Decorator for Entity mod dependency"""
    def wrap(cl):
        for mod in mods:
            cl.dep_mod(mod)
        return cl
    return wrap

@add_metaclass(EntityMeta)
class Entity(object):
    """Base entity, including dynamic property and modding mechanism.
    
    Do not create class hierarchy. All entity classes should inherit this
    directly and use @mod_dep for dependencies.
    """
    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__()
        self._props = dict()
        self._listeners = dict()
        self._methods = set()
        # TODO: fix this
        self._priorities = ('early', 'normal', 'late')
        self._default = 'normal'
        self._mods = list([type(self)])
        self._mods_amount = dict({type(self):1})
        self._get_depends_on = {}
        fix_methods(self)
        self._init_depmods()
        self._init(*args, **kwargs)
        self._load()
        self._load_patchmods()
    
    @unbound
    def _init(self):
        """This is used to init Entity or to add it as mod.
        
        Use it instead of __init__
        """
        pass
    
    @unbound
    def _save(self):
        """This is called before pickling (for every mod)
        
        Any data that is not essential for saving can be get rid of at
        this point.
        """
        pass
    
    @unbound
    def _load(self):
        """This is called after pickling and after _init when creating
        
        NOTE: mods & dynamic properties will be restored automatically,
        but property nodes should be assigned here.
        """
        pass
    
    @unbound
    def _uninit(self):
        """This is called when unloading mod.
        
        You should implement this in your unloadable mod if you use `_init`.
        `_uninit` is implemented for declarative mods
        """
        pass
    
    @classmethod
    def dep_mod(cl, mod):
        """Add mod dependency for this Entity class"""
        cl._mod_deps.append(mod)
    
    @classmethod
    def global_mod(cl, mod):
        """Add global mod to this Entity class.
        
        This mod will be automatically added to all instances created or
        loaded after calling global_mod
        """
        cl._global_mods.append(mod)
    
    @unbound
    def _init_depmods(self, cl=None):
        if cl is None:
            cl = type(self)
        mods = DependencyTree.collect(cl, get_mods_deps)
        for mod in mods:
            self.req_mod(mod)
    
    @unbound
    def _load_depmods(self, cl=None):
        if cl is None:
            cl = type(self)
        mods = DependencyTree.collect(cl, get_mods_deps)
        for mod in mods:
            self.load_mod(mod)
    
    @unbound
    def _load_patchmods(self, cl=None):
        if cl is None:
            cl = type(self)
        mods = cl._global_mods
        for mod in mods:
            mod_deps = DependencyTree.collect(mod, get_mods_deps)
            for dep in mod_deps:
                self.req_mod(dep)
            self.req_mod(mod)
    
    def __getattr__(self, name):
        if name == '_props':
            raise AttributeError('_props not present!')
        if name in self._props:
            return self._props[name].value
        try:
            self_repr = repr(self)
        except AttributeError:
            self_repr = 'this entity'
        raise AttributeError('{} has no attribute/property {}'.format(self_repr, name))
    
    def __setattr__(self, name, value):
        if name[0] == '_':
            super(Entity, self).__setattr__(name, value)
        elif name in self._props:
            self._props[name].value = value
            self.notify_listeners(name)
        elif name in self._methods:
            method = functools.partial(value, self)
            functools.update_wrapper(method, value)
            super(Entity, self).__setattr__(name, method)
        else:
            super(Entity, self).__setattr__(name, value)
            #raise AttributeError('{} has no property {}'.format(self, name))
    
    def __str__(self):
        return 'Entity {}'.format({name:getattr(self, name) for name in self._props})
    
    def __repr__(self):
        return 'Entity of type {} with mods {}'.format(type(self).__name__, [mod.__name__ for mod in self._mods])
    
    def __getstate__(self):
        self_copy = self.__dict__.copy()
        # can't save methods, but they'll be restored by mods
        for name in self._methods:
            del self_copy[name]
        # will be restored by mods as well
        del self_copy['_listeners']
        self_copy['_mods_to_load'] = [
            mod
                for mod in self_copy['_mods']
                    if not mod in type(self)._global_mods and not mod is type(self)
            ]
        del self_copy['_mods']
        return self_copy
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._mods = list([type(self)])
        self._mods_amount = dict({type(self):1})
        self._listeners = dict({prop:list() for prop in self._props})
        self._load_depmods()
        self._load()
        for mod in self._mods_to_load:
            self.load_mod(mod)
        self._load_patchmods()
    
    @classmethod
    def enable(cl, target, first_load, *args, **kwargs):
        """Enable this mod on target entity (internal use)"""
        for attr in cl.__dict__:
            if attr[0] != '_':
                if first_load and (attr in target._props or attr in target._methods):
                    raise AttributeError('Attribute with name {} already exist on {}'.format(attr, target))
                target.dynamic_method(attr)
                setattr(target, attr, cl.__dict__[attr])
        if first_load:
            cl._init(target, *args, **kwargs)
        cl._load(target)
        cl._load_patchmods(target, cl)
    
    @classmethod
    def disable(cl, target):
        """Disable this mod on target entity (internal use)"""
        cl._uninit(target)
    
    def dynamic_method(self, name):
        self._methods.add(name)
    
    def dynamic_property(self, name, empty=None, priorities=None):
        """Define new dynamic property called name"""
        if name in self._props:
            return
        if priorities is None:
            priorities = self._priorities
        self._props[name] = DynamicProperty(self, empty=empty, priorities=priorities, default=self._default)
        self._get_depends_on[name] = dict()
        self._listeners[name] = list()
    
    def remove_property(self, name):
        """Remove dynamic property. To use in mod.disable()"""
        del self._props[name]
        del self._get_depends_on[name]
    
    def load_mod(self, mod):
        """Load mod to this entity after reloading (for internal use)"""
        self.req_mod(mod, first_load=False)
    
    def req_mod(self, mod, args=(), kwargs={}, first_load=True):
        """Add mod to this entity (for internal use)"""
        if not mod in self._mods:
            self._mods.append(mod)
            self._mods_amount[mod] = 1
            mod.enable(self, first_load, *args, **kwargs)
        else:
            self._mods_amount[mod] += 1
    
    def add_mod(self, mod, *args, **kwargs):
        """Add mod dynamically"""
        mod_deps = DependencyTree.collect(mod, get_mods_deps)
        for dep in mod_deps:
            if dep != mod:
                self.req_mod(dep)
        self.req_mod(mod, args, kwargs)
    
    def del_mod(self, mod):
        """Remove mod dynamically"""
        mod_deps = DependencyTree.collect(mod, get_mods_deps)
        for dep in mod_deps:
            self._mods_amount[dep] -= 1
            if self._mods_amount[dep] <= 0:
                dep.disable(self)
                self._mods.remove(dep)
    
    def has_mod(self, mod):
        """Check if this Entity has mod.
        
        Still, duck typing is usually preferred cause same behaviour can
        be implemented by different mods.
        """
        return mod in self._mods
    
    def no_set(self, prop):
        """Forbid setting prop"""
        self.add_set_node(prop, ForbidWritingNode(prop))
    
    def add_set_node(self, prop, node, priority=None):
        """Add setter node"""
        self._props[prop].add_set_node(node, priority)
    
    def add_get_node(self, prop, node, priority=None):
        """Add getter node"""
        self._props[prop].add_get_node(node, priority)
        for dependency in node.deps():
            self.inc_get_dependency(dependency, prop)
        try:
            getattr(self, prop)
        except RuntimeError:
            raise NodeDependencyError('circular dependency on {}'.format(prop))
    
    def del_set_node(self, prop, node):
        self._props[prop].del_set_node(node)
    
    def del_get_node(self, prop, node):
        self._props[prop].del_get_node(node)
        for dependency in node.deps():
            self.dec_get_dependency(dependency, prop)
    
    def inc_get_dependency(self, dependency, dependant):
        if not dependant in self._get_depends_on[dependency]:
            self._get_depends_on[dependency][dependant] = 0
        self._get_depends_on[dependency][dependant] += 1
    
    def dec_get_dependency(self, dependency, dependant):
        if not dependant in self._get_depends_on[dependency]:
            self._get_depends_on[dependency][dependant] = 0
        else:
            self._get_depends_on[dependency][dependant] -= 1
    
    def add_listener_node(self, prop, listener):
        """Add listner node to the prop.
        
        It will be notified on changes, including changes of dependencies.
        """
        self._listeners[prop].append(listener)
    
    def notify_listeners(self, prop):
        """Notify listeners of prop, including those who depend on it.
        
        NOTE: this may lead to some listener getting notified more than once if
        it's dependency of multiple dependencies.
        """
        getattr(self, prop)
        for listener in self._listeners[prop]:
            listener(self, getattr(self, prop))
        for dep in self._get_depends_on[prop]:
            self.notify_listeners(dep)

class NodeDependencyError(AttributeError):
    pass

class ProcessingNode(object):
    def __init__(self):
        super(ProcessingNode, self).__init__()
        self._depends = set()
    
    def depends(self, prop):
        self._depends.add(prop)
    
    def deps(self):
        return self._depends.copy()
    
    def __call__(self, target, value):
        return value

class ListenerNode(ProcessingNode):
    def __init__(self, f):
        super(ListenerNode, self).__init__()
        self.f = f
    
    def __str__(self):
        return '<ListenerNode with {}>'.format(str(self.f))
    
    def __repr__(self):
        return str(self)
    
    def __call__(self, target, value):
        self.f(target, value)

def listener(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        return ListenerNode(curry.curry(f)(*args, **kwargs))
    return wrap

class ReadOnlyNode(ProcessingNode):
    """Processing node with only limited read access"""
    def __init__(self):
        super(ReadOnlyNode, self).__init__()
    
    def __call__(self, target, value):
        kwargs = {name : getattr(target, name) for name in self.deps()}
        kwargs.update({'value' : value})
        return self.process(**kwargs)
    
    def process(self, value, **kwargs):
        return value

class SimpleNode(ReadOnlyNode):
    def __init__(self, f):
        super(SimpleNode, self).__init__()
        self.f = f
    
    def process(self, value, **kwargs):
        return self.f(value, **kwargs)

def simplenode(f):
    """Returns function, which returns SimpleNode
    
    >>> from dracykeiton.entity import simplenode, SimpleNode
    >>> node = simplenode(int)(base=2)
    >>> isinstance(node, SimpleNode)
    True
    
    >>> @simplenode
    ... def foo(a, b, value):
    ...     return (a+b)*value
    >>> foo(1, 2).process(5)
    15
    """
    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        return SimpleNode(functools.partial(f, *args, **kwargs))
    return wrap

def writernode(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        return SimpleNode(functools.partial(f, *args, **kwargs))
    return wrap

def depends(*names):
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            node = f(*args, **kwargs)
            for name in names:
                node.depends(name)
            return node
        return wrap
    return decorator

class ForbidWritingNode(ReadOnlyNode):
    def __init__(self, prop):
        super(ForbidWritingNode, self).__init__()
        self.prop = prop
    
    def process(self, value):
        raise AttributeError('property {} cannot be accessed'.format(self.prop))
