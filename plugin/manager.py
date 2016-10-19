"""
This class defines how plugins are created from a folder.
"""
import imp
import os
import os.path


PLUGIN_FILE_EXTENSION = '.py'
PLUGIN_METADATA_CLASS = 'PluginMetadata'
PLUGIN_KEY_SEPARATOR = '.'


class PluginMetadataInterface(object):
    """Interface for all plugins adde to the plugin manager."""
    def __init__(self):
        pass

    def category(self):
        """Retrieves the category name for the plugin."""
        pass

    def name(self):
        """Retrieves the category implementation name for the plugin."""
        pass

    def priority(self):
        """
        Retrieves the priority of the implementation for the plugin for
        default plugin selection.
        """
        pass

    def create_instance(self, options=None):
        """Factor for this specific plugin instance."""
        pass


class PluginManager(object):
    """This class defines how plugins are created from a folder. """
    @classmethod
    def safe_remove_file(cls, filename):
        """Remove a filename suppressing any exceptions."""
        if os.path.isfile(filename):
            os.unlink(filename)

    @classmethod
    def _make_key(cls, category, name):
        """Create a key from the category and provider name."""
        if category is None or name is None:
            err = 'Neither the "category" or the "name" are allowed to be ' \
                  '"None"!'
            raise RuntimeWarning(err)
        return '{}{}{}'.format(category, PLUGIN_KEY_SEPARATOR, name)

    @classmethod
    def _split_key(cls, key):
        """Split the key into category and provider name."""
        return key.split(PLUGIN_KEY_SEPARATOR)

    def __init__(self, plugin_folder=None):
        """Constructor that may add the first folder of plugins."""
        self.__plugin_files = []
        self.__provider_categories = dict()
        if plugin_folder is not None:
            self.add_plugin_folder(plugin_folder)

    def add_plugin_folder(self, plugin_folder):
        """Add a folder of plugins to the manager."""
        for filename in os.listdir(plugin_folder):
            if os.path.splitext(filename)[1] == PLUGIN_FILE_EXTENSION:
                full = os.path.join(plugin_folder, filename)
                self._add_plugin(full)

    def _add_plugin(self, fullname):
        """Add the plugin to the dictionary."""
        if fullname not in self.__plugin_files:
            if self._load_metadata(fullname):
                self.__plugin_files.append(fullname)

    def _load_metadata(self, plugin_filename):
        """Load the plugin dynamically."""
        path_name, base_filename = os.path.split(plugin_filename)
        module_name = os.path.splitext(base_filename)[0]
        compiled = os.path.join(path_name, "%s.pyc" % module_name)
        PluginManager.safe_remove_file(compiled)
        module = imp.load_source(module_name, plugin_filename)
        if hasattr(module, PLUGIN_METADATA_CLASS):
            meta_obj = getattr(module, PLUGIN_METADATA_CLASS)()
            self.add_provider(meta_obj)
            return True
        return False

    def add_provider(self, meta):
        """Add this provider to the list."""
        key = PluginManager._make_key(meta.category(), meta.name())
        if key in self.__provider_categories.keys():
            if meta.priority() == self.__provider_categories[key].priority():
                err = 'There is a collision of category providers and ' \
                      'priority. The same named provider in a category ' \
                      'cannot have equal priority.'
                raise RuntimeWarning(err)
            elif meta.priority() < self.__provider_categories[key].priority():
                self.__provider_categories[key] = meta
        else:
            self.__provider_categories[key] = meta

    def get_categories(self):
        """Retrieve the list of unique provider categories."""
        categories = []
        for key in self.__provider_categories.keys():
            category = PluginManager._split_key(key)[0]
            if category not in categories:
                categories.append(category)
        return categories

    def get_sorted_providers(self, category):
        """Retrieve the list of providers for a category."""
        providers = []
        for key in self.__provider_categories.keys():
            stored_category, name = PluginManager._split_key(key)
            if category == stored_category:
                providers.append((self.__provider_categories[key].priority(),
                                  name))
        providers.sort()
        provider_list = []
        for item in providers:
            provider_list.append(item[1])
        return provider_list

    def factory_create_instance(self, category, name=None, options=None):
        """Create a named (or default) provider in the specified category."""
        if category is None:
            return None
        if name is None:
            categories = self.get_sorted_providers(category)
            if categories is not None and len(categories) > 0:
                name = categories[0]
        if name is None or category is None:
            return None
        key = PluginManager._make_key(category, name)
        factory_obj = self.__provider_categories[key]
        return factory_obj.create_instance(options=options)
