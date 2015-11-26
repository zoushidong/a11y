#/usr/bin/python

import dbus.exceptions
import dbus.service
import dbus.mainloop.glib
import dbus.glib

class Unity(object):
	dbgbus_name = 'com.canonical.Unity'
	dbgbus_path = '/com/canonical/Unity/Debug/Introspection'
	dbgbus_interface = 'com.canonical.Unity.Debug.Introspection'
	_state = None

	def __init__(self):
		self._bus = dbus.SessionBus()
		self._proxyobj = self._bus.get_object(self.dbgbus_name,
						      self.dbgbus_path)
		self._dbgiface = dbus.Interface(self._proxyobj,
		                                self.dbgbus_interface)
		self._state = None

	def get_state(self, UIElement = None):
		"""Dump the state of the UIElement

		UIElement: Launcher, Panel, ... or All is None or Unity
		"""
		self._state = self._dbgiface.GetState(UIElement)
		return self._state

	def walk_state(self, data = None, level=0):
		""" Dump the state in a human readable format

		data: If None uses self._state
		level: Level of the node
		"""
		if data is None:
			data = self._state

		level += 1
		if isinstance(data, dbus.Dictionary):
			for k, v in data.iteritems():
				print "  " * level, k
				self.walk_state(v, level)
		elif isinstance(data, dbus.Struct):
			for v in data:
				#print "  " * level, v
				self.walk_state(v, level)
		else:
			print "  " * level, data

def runtest():
	u = Unity()
	s = u.get_state('panel')
	u.walk_state()

if __name__ == '__main__':
	runtest()
