"""TestRobot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from Apps import xadmin
from Case import views as Cviews
from Yaml import views as Yviews
from Tag import views as Tviews
from TestRobot.settings import STATIC_ROOT, MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^test/bdd/createbusiness', Cviews.createbusiness, name='createbusiness'),
    url(r'^test/bdd/createsuitebdd', Cviews.createsuitebdd, name='runsuitebdd'),
    url(r'^test/bdd/runsuitebdd', Cviews.runsuitebdd, name='runsuitebdd'),
    url(r'^test/sort', Cviews.sort, name='sort'),
    url(r'^test/singlecase', Cviews.runsinglecase, name='singlecase'),
    url(r'^test/bdd', Cviews.bdd, name='bdd'),
    url(r'^test/ddd', Cviews.ddd, name='ddd'),
    url(r'^yaml/editfile', Yviews.editfile, name='editfile'),
    url(r'^yaml/edittag', Yviews.edittag, name='edittag'),
    url(r'^yaml/editpath', Yviews.editpath, name='editpath'),
    url(r'^yaml/editparam', Yviews.editparam, name='editparam'),
    url(r'^yaml/', Yviews.yaml, name='yaml'),
    url(r'^generator/initdir', Tviews.initdir, name='initdir'),
    url(r'^generator/initbusiness', Tviews.initbusiness, name='initbusiness'),
    url(r'^generator/', Tviews.generator, name='generator'),
    url(r'^$', Cviews.index, name='index'),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT, 'show_indexes': True}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT, 'show_indexes': True}),
]
