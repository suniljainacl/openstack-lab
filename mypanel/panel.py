from django.utils.translation import gettext_lazy as _
import horizon


class MyPanel(horizon.Panel):
    name = _("My Lab Info")
    slug = "mypanel"


horizon.get_dashboard("project").register(MyPanel)
