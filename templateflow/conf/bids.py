"""Extending pyBIDS for querying TemplateFlow."""
from pkg_resources import resource_filename
from bids.layout import BIDSLayout, add_config_paths

add_config_paths(templateflow=resource_filename("templateflow", "conf/config.json"))


class Layout(BIDSLayout):
    def __repr__(self):
        # A tidy summary of key properties
        s = """\
TemplateFlow Layout
 - Home: {}
 - Templates: {}.""".format(
            self.root, ", ".join(sorted(self.get_templates()))
        )
        return s
