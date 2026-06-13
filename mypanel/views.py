from django.views import generic
from django.utils.translation import gettext_lazy as _


class IndexView(generic.TemplateView):
    template_name = "mypanel/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_info'] = {
            'student': 'Sunil',
            'vm_host': 'controller',
            'private_ip': '10.0.0.4',
            'os': 'Ubuntu 24.04 LTS',
            'openstack_version': '2026.1 Gazpacho',
            'services': [
                'Keystone (Identity) - port 5000',
                'Glance (Images) - port 9292',
                'Placement (Resources) - port 8778',
                'Nova (Compute) - port 8774',
                'Neutron (Networking) - port 9696',
                'Cinder (Block Storage) - port 8776',
                'Horizon (Dashboard) - port 80',
            ]
        }
        return context
