import platform
import time

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from django.core.management import call_command

from django.conf import settings

from django.test.client import RequestFactory

from omero_qa.registry.views import hit as views_hit
from omero_qa.registry.models import Agent, IP, Hit, Continents, Version


def getOSVersion():
    try:
        if len(platform.mac_ver()[0]) > 0:
            version = "%s;%s" % (platform.platform(),
                                 platform.mac_ver()[0])
        else:
            version = platform.platform()
    except:
        version = platform.platform()
    return version


class RegistryTestCase(TestCase):

    def setUp(self):
        Version.objects.create(version="1.2.3")
        Agent.objects.create(agent_name="OMERO.test", display_name="OMERO.test")
        self.factory = RequestFactory()

    def test_empty_hit(self):
        hit_url = reverse('registry_hit')
    
        response = self.client.get(hit_url)
        self.assertEqual(response.status_code, 302)

    def test_bad_agent(self):
        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, HTTP_USER_AGENT='foo')
        response = views_hit(request)
        self.assertEqual(response.status_code,302)

    def test_old_version(self):
        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = '0.0.0'
        data["os.name"] = platform.system()
        data["os.arch"] = platform.machine()
        data["os.version"] = getOSVersion()
        data["python.version"] = platform.python_version()
        data["python.compiler"] = platform.python_compiler()
        data["python.build"] = platform.python_build()

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data, HTTP_USER_AGENT='OMERO.test')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Please upgrade to %s. See http://downloads.openmicroscopy.org/latest-stable/omero for the latest version.' % ver.version)

        hit = Hit.objects.get(agent_version=data["version"])
        self.assertEqual(hit.os_name, data["os.name"])
        self.assertEqual(hit.os_arch, data["os.arch"])
        self.assertEqual(hit.os_version, data["os.version"])
        self.assertEqual(hit.python_version, data["python.version"])
        self.assertEqual(hit.python_compiler, data["python.compiler"][:50])
        self.assertEqual(hit.python_build, data["python.build"][1])

    def test_current_version(self):
        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version
        data["os.name"] = platform.system()
        data["os.arch"] = platform.machine()
        data["os.version"] = getOSVersion()
        data["python.version"] = platform.python_version()
        data["python.compiler"] = platform.python_compiler()
        data["python.build"] = platform.python_build()
    
        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data, HTTP_USER_AGENT='OMERO.test')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agent_version=data["version"])
        self.assertEqual(hit.os_name, data["os.name"])
        self.assertEqual(hit.os_arch, data["os.arch"])
        self.assertEqual(hit.os_version, data["os.version"])
        self.assertEqual(hit.python_version, data["python.version"])
        self.assertEqual(hit.python_compiler, data["python.compiler"][:50])
        self.assertEqual(hit.python_build, data["python.build"][1])

