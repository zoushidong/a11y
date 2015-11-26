from pyatspi import Registry
from logging import info

reg = Registry

def callback(event):
    reg.stop()
    info(event)

def event_listener(event_cate, event_name):
    """
    event_cate: event categories, say "document"
    event_name: event names, say "document:load-complete"
    """
    reg.registerEventListener(callback,event_cate,event_name)
    reg.start()
    reg.deregisterEventListener(callback,event_cate,event_name)
    return True
