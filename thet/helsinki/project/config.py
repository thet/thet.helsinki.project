PROJECTNAME = "thet.helsinki.project"

ADD_PERMISSIONS = {
    "Project": "thet.helsinki.project: Add Project",
}

from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Owner', 'Contributor'))
