from importlib.resources import files

from sfdata import SFDataFile, SFProcFile, SFScanInfo
from sfdata.sfchannel import SFChannel

from yokai import Plugin, read_instance_dict, read_markdown
from yokai import YokAI as CoreYokAI


FAQ_FILE = files(__package__) / "FAQ.md"

PARAGRAPH = read_markdown(files(__package__) / "paragraph.md")

# the attribute identifying instances of each type (and its subclasses, e.g. SFChannelJF)
IDENTIFYING_ATTRIBUTES = {
    SFChannel: "name",
    SFDataFile: "fname",
    SFProcFile: "fname",
    SFScanInfo: "fname"
}


class YokAI(CoreYokAI):
    """
    YokAI for sfdata sessions
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, plugins=[SFDataPlugin()], **kwargs)



class SFDataPlugin(Plugin):
    """
    Tells YokAI about sfdata:
    An sfdata session, sfdata's FAQ, its README,
    and sfdata objects: channels identified by name, scans and files by path.
    """

    module_prefix = "sfdata"
    faq_file = FAQ_FILE
    paragraph = PARAGRAPH

    def identification(self, obj):
        attr = find_identifying_attribute(obj)
        if attr is None:
            return {}
        attrs = read_instance_dict(obj)
        return {attr: attrs.get(attr)}



def find_identifying_attribute(obj):
    # type(obj), never obj.__class__, which may be any object
    cls = type(obj)
    for identified_type, attr in IDENTIFYING_ATTRIBUTES.items():
        if issubclass(cls, identified_type):
            return attr
    return None



