from Products.Five import BrowserView
from zope.component import getMultiAdapter


class ProjectView(BrowserView):
    @property
    def plone_view(self):
        plone_view = getMultiAdapter((self.context, self.request), name="plone")
        return plone_view

    @property
    def date(self):
        ret = None

        start = self.context.start()
        end = self.context.end()

        if start.Date() == end.Date():
            return self.plone_view.toLocalizedTime(start)

        ret = "%s - %s" % (
            self.plone_view.toLocalizedTime(start),
            self.plone_view.toLocalizedTime(end),
        )

        return ret
