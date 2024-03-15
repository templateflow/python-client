"""Extending pyBIDS for querying TemplateFlow."""
from bids.layout import BIDSLayout, add_config_paths

from . import load_data

add_config_paths(templateflow=load_data('config.json'))


class Layout(BIDSLayout):
    def __repr__(self):
        # A tidy summary of key properties
        s = """\
TemplateFlow Layout
 - Home: {}
 - Templates: {}.""".format(
            self.root, ', '.join(sorted(self.get_templates()))
        )
        return s
