# GConf wrapper 
# Modified from Johan Dahlin's code:
# http://www.daa.com.au/pipermail/pygtk/2002-August/003220.html
import gconf
from gconf import VALUE_BOOL, VALUE_INT, VALUE_STRING, VALUE_FLOAT
from types import StringType, IntType, FloatType, BooleanType

class GConf:
    """
    This class provides a handy interface for manipulating a gconf key.

    >>> from gconfwrapper import GConf
    >>> interface=GConf("/desktop/gnome/interface/")
    >>> interface["accessibility"]
    False
    >>> interface["gtk_theme"]="Human"

    This class can also be used without being instantiated.

    >>> GConf.get_item('/desktop/gnome/interface/accessibility')
    False
    >>> GConf.set_item('/desktop/gnome/interface/accessibility')

    The instance methods support the __getitem__ and __setitem__ special methods
    automatically invoke get_item and set_item to handle properties. Generally,
    instance methods should not be called directly.

    The static methods are for convenience, avoiding instance instantiation when
    getting or setting only a single gconf key.

    @group Automatically invoked accessors: *value, *string, *bool, *int,
        *float, __getitem__, __setitem__, _get_type
    """


    class GConfError(Exception):
        """
        Exception class for GConf exceptions
        """
        pass

    def __init__ (self, domain):
        """
        Constructor for the GConf class

        @param domain: The GConf domain, for instance: /desktop/gnome/interface/
        @type domain: string
        """
        self._domain = domain
        self._gconf_client = gconf.client_get_default ()

    def __getitem__ (self, attr):
        return self.get_value (attr)

    def __setitem__ (self, key, val):
        self.set_value (key, val)

    def _get_type (self, key):
        KeyType = type (key)
        if KeyType == StringType:
            return 'string'
        elif KeyType == IntType:
            return 'int'
        elif KeyType == FloatType:
            return 'float'
        elif KeyType == BooleanType:
            return 'bool'
        else:
            raise self.GConfError, 'unsupported type: %s' % str (KeyType)

    # Public functions

    def set_domain (self, domain):
        """
        Change the domain of the current GConf instance

        @param domain: New domain to use
        @type domain: string
        """
        self._domain = domain

    def get_domain (self):
        """
        Get the domain of the current GConf instance

        @return: Domain of the current GConf instance
        @rtype: string
        """
        return self._domain

    def get_gconf_client (self):
        """
        Access the pygtk GConf client

        @return: The pygtk GConf client
        @rtype: pygtk gconf object
        """
        return self._gconf_client

    def get_value (self, key):
        '''
        Returns the value of key 'key'

        This is automatically invoked by the instance __getitem__ and
        __setitem__ so should not need to be called directly.

        @param key: Target key to get
        @type key: string
        @return: Current value of target key
        @rtype: bool, int, string, float
        '''
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        value = self._gconf_client.get (self._domain + key)
        ValueType = value.type
        if ValueType == VALUE_BOOL:
            return value.get_bool ()
        elif ValueType == VALUE_INT:
            return value.get_int ()
        elif ValueType == VALUE_STRING:
            return value.get_string ()
        elif ValueType == VALUE_FLOAT:
            return value.get_float ()

    def set_value (self, key, value):
        '''
        Sets the value of key 'key' to 'value'

        This is automatically invoked by the instance __getitem__ and
        __setitem__ so should not need to be called directly.

        @param key: Target key to set
        @type key: string
        @param value: Value to set
        @type value: bool, int, string, float
        '''
        value_type = self._get_type (value)

        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        func = getattr (self._gconf_client, 'set_' + value_type)
        apply (func, (self._domain + key, value))

    def get_string (self, key):
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        return self._gconf_client.get_string (self._domain + key)

    def set_string (self, key, value):
        if type (value) != StringType:
            raise self.GConfError, 'value must be a string'
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        self._gconf_client.set_string (self._domain + key, value)

    def get_bool (self, key):
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        return self._gconf_client.get_bool (self._domain + key)

    def set_bool (self, key, value):
        if type (value) != IntType and \
            (key != 0 or key != 1):
            raise self.GConfError, 'value must be a boolean'
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        self._gconf_client.set_bool (self._domain + key, value)

    def get_int (self, key):
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        return self._gconf_client.get_int (self._domain + key)

    def set_int (self, key, value):
        if type (value) != IntType:
            raise self.GConfError, 'value must be an int'
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        self._gconf_client.set_int (self._domain + key, value)

    def get_float (self, key):
        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        return self._gconf_client.get_float (self._domain + key)

    def set_float (self, key, value):
        if type (value) != FloatType:
            raise self.GConfError, 'value must be an float'

        if '/' in key:
            raise self.GConfError, 'key must not contain /'

        self._gconf_client.set_float (self._domain + key, value)

    # Some even simpler methods for the truly lazy
    @staticmethod
    def get_item(key):
        """
        Pass this a key and it will return the value

        >>> GConf.get_item("/desktop/gnome/interface/accessibility")
        True

        @type key:  string
        @param key: The gconf path to the target key
        @rtype:     string, int, bool, float
        @return:    The contents of the specified key
        """
        dirname="%s/" % key.rpartition('/')[0]
        keyname=key.rpartition('/')[2]
        g=GConf(dirname)
        return g[keyname]
        
    @staticmethod
    def set_item(key, value):
        """
        Set key to value provided

        >>> GConf.set_item("/desktop/gnome/interface/accessibility", True)

        @type key:      string
        @param key:     The gconf path to the target key
        @type value:    string, int, bool, float
        @param value:   The desired new value of the specified key
        """
        dirname="%s/" % key.rpartition('/')[0]
        keyname=key.rpartition('/')[2]
        g=GConf(dirname)
        g[keyname]=value   

def test():
    c=GConf ('/apps/test-gconf/')
    c['foo']='1'
    c['bar']=2
    c['baz']=3.1

    print c['foo'], c['bar'], c['baz']
    print "Accessibility: %s" % GConf.get_item('/desktop/gnome/interface/accessibility')
    GConf.set_item('/apps/test-gconf/foobar', True)
    GConf.set_item('/apps/test-gconf/barfoo', False)

if __name__ == '__main__':
    test()
