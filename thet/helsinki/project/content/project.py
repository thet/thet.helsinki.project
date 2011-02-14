from zope.interface import implements
from AccessControl import ClassSecurityInfo
try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View

from collective.folderishtypes.content import folderish_event

from thet.helsinki.project.interfaces import IProject
from thet.helsinki.project.config import PROJECTNAME
from thet.helsinki.project import MsgFact as _

from plone.app.imaging.utils import getAllowedSizes
allowed_sizes = getAllowedSizes()

ct_schema = folderish_event.ct_schema.copy() + atapi.Schema((
    atapi.ImageField('image',
        required=False,
        storage = atapi.AnnotationStorage(migrate=True),
        languageIndependent=True,
        sizes = allowed_sizes,
        widget=atapi.ImageWidget(
            description = _(u'help_project_image',
                default=u'The project image will be shown in listings and in the project detail view itself.'),
            label= _(u'label_project_image', default=u'Image'),
            ),
        ),
    atapi.StringField('imageCaption',
        required = False,
        searchable = True,
        widget = atapi.StringWidget(
            description = '',
            label = _(u'label_image_caption', default=u'Image Caption'),
            size = 40)
        ),
))

schemata.finalizeATCTSchema(ct_schema,
                            folderish=True,
                            moveDiscussion=False)

class Project(folderish_event.FolderishEvent):
    implements(IProject)

    portal_type = 'Project'
    _at_rename_after_creation = True
    schema = ct_schema

    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image
        return folderish_event.FolderishEvent.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(Project, PROJECTNAME)
