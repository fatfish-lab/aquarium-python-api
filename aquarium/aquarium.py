# -*- coding: utf-8 -*-
from . import JSON_CONTENT_TYPE
from .item import Item
from .edge import Edge
from .utils import evaluate
from .items.user import User
from .items.template import Template
from .items.project import Project
from .items.task import Task
from .items.shot import Shot
from .items.asset import Asset
from .items.usergroup import Usergroup
from .items.organisation import Organisation
from .element import Element

import requests

import sys
if sys.version_info[0] > 2:
    from urllib.parse import urljoin, urlparse
else:
    from urlparse import urljoin, urlparse

import json
import logging
logger=logging.getLogger(__name__)


class Aquarium(object):
    """
    This class describes the main class of Aquarium

    :param api_url: Specify the URL of the API.
    :type api_url: string
    :param token: Specify the authentication token, to avoid :func:`~aquarium.aquarium.Aquarium.connect`
    :type token: string, optional
    :param api_version: Specify the API version you want to use (default : `v1`).
    :type api_version: string, optional

    :ivar token: Get the current token (populated after a first :func:`~aquarium.aquarium.Aquarium.connect`)
    :ivar edge: Access to :class:`~aquarium.edge.Edge`
    :ivar item: Access to :class:`~aquarium.item.Item`
    :ivar asset: Access to subclass :class:`~aquarium.items.asset.Asset`
    :ivar project: Access to subclass :class:`~aquarium.items.project.Project`
    :ivar shot: Access to subclass :class:`~aquarium.items.shot.Shot`
    :ivar task: Access to subclass :class:`~aquarium.items.task.Task`
    :ivar template: Access to subclass :class:`~aquarium.items.template.Template`
    :ivar user: Access to subclass :class:`~aquarium.items.user.User`
    :ivar usergroup: Access to subclass :class:`~aquarium.items.usergroup.Usergroup`
    :ivar organisation: Access to subclass :class:`~aquarium.items.organisation.Organisation`
    """

    def __init__(self, api_url='', token='', api_version='v1'):
        """
        Constructs a new instance.
        """
        # Session
        self.session=requests.Session()

        self.api_url=api_url
        self.api_version=api_version
        self.token=token
        # Classes
        self.element=Element(parent=self)
        self.item=Item(parent=self)
        self.edge=Edge(parent=self)
        # SubClasses
        self.user=User(parent=self)
        self.usergroup=Usergroup(parent=self)
        self.organisation=Organisation(parent=self)
        self.template=Template(parent=self)
        self.project=Project(parent=self)
        self.task=Task(parent=self)
        self.shot=Shot(parent=self)
        self.asset=Asset(parent=self)

    def do_request(self, *args, **kwargs):
        """
        Execute a request to the API

        :param      args:    Parameters used to send the request : HTTP verb, API endpoint
        :type       args:    tuple
        :param      kwargs:  Headers, data and parameters used for the request
        :type       kwargs:  dictionary

        :returns:   Request response
        :rtype:     List or dictionary
        """
        token=self.token

        decoding=True
        if 'decoding' in kwargs:
            decoding=kwargs.pop('decoding')

        if 'headers' in kwargs:
            headers=kwargs.pop('headers')
            if headers is not None:
                headers.update(dict(authorization=token))
        else:
            headers=dict(authorization=token)
            headers.update(JSON_CONTENT_TYPE)

        args=list(args)
        typ=args[0]
        path = self.api_url

        if len(args) > 1:
            is_files = args[1].find('/files/') >= 0
            if (is_files):
                path = urljoin(path, args[1])
            else:
                path = urljoin(path, '{api_version}/{endpoint}'.format(
                    api_version=self.api_version,
                    endpoint=args[1]
                ))
        else:
            path = urljoin(path, self.api_version)

        logger.debug('Send request : %s %s', typ, path)
        self.session.headers.update(headers)
        response=self.session.request(typ, path, **kwargs)
        evaluate(response)
        if decoding:
            response=response.json()
        return response

    def cast(self, data={}):
        """
        Creates an item or edge instance from a dictionary

        :param      data:         The object item or edge from Aquarium API
        :type       data:         dictionary

        :returns:   Instance of Edge or Item or items subclass
        :rtype:     :class:`~aquarium.edge.Edge` | :class:`~aquarium.item.Item` : [:class:`~aquarium.items.asset.Asset` | :class:`~aquarium.items.project.Project` | :class:`~aquarium.items.shot.Shot` | :class:`~aquarium.items.task.Task` | :class:`~aquarium.items.template.Template` | :class:`~aquarium.items.user.User` | :class:`~aquarium.items.usergroup.Usergroup`]
        """
        value=data
        #As Entity
        if data and '_id' in data.keys():
            id=data.get('_id')
            cls=None
            #As Item
            if id.split('/')[0]=='items':
                type=data.get('type')
                if type=='Project':
                    cls=self.project
                elif type=='User':
                    cls=self.user
                elif type=='Template':
                    cls=self.template
                elif type=='Usergroup':
                    cls=self.usergroup
                elif type=='Asset':
                    cls=self.asset
                elif type=='Shot':
                    cls=self.shot
                elif type=='Task':
                    cls=self.task
                elif type=='Organisation':
                    cls=self.organisation
                else:
                    cls=self.item
            #As Edge
            elif id.split('/')[0]=='connections':
                cls=self.edge
            if cls is not None:
                value=cls(data=data)

        return value

    def signin(self, email='', password=''):
        """
        Sign in a user with its email and password

        :param      email:     The email of the user
        :type       email:     string
        :param      password:  The password of the user
        :type       password:  string
        """
        return self.user.signin(email=email, password=password)

    def connect(self, email='', password=''):
        """
        Alias of :func:`~aquarium.aquarium.Aquarium.signin`
        """
        return self.user.signin(email=email, password=password)

    def signout(self):
        """
        Sign out current user by clearing the stored authentication token

        .. note::
            After a :func:`~aquarium.aquarium.Aquarium.signout`, you need to use a :func:`~aquarium.aquarium.Aquarium.signin` before sending authenticated requests

        :returns: None
        """
        logger.info('Disconnect current user')
        logger.debug('Clear authentication token for logout')
        self.user.signout()

    def logout(self):
        """
        Alias of :func:`~aquarium.aquarium.Aquarium.signout`
        """
        self.signout()

    def me(self):
        """
        Alias of :func:`~aquarium.aquarium.Aquarium.get_current_user`


        :returns:   A :class:`~aquarium.items.user.User` instance of the connected user.
        :rtype:     :class:`~aquarium.items.user.User` object
        """
        return self.get_current_user()

    def get_current_user(self):
        """
        Alias of :func:`~aquarium.items.user.User.get_current`


        :returns:   A :class:`~aquarium.items.user.User` instance of the connected user.
        :rtype:     :class:`~aquarium.items.user.User` object
        """
        result=self.user.get_current()
        return result

    def mine(self):
        """
        Alias of :func:`~aquarium.items.user.User.get_profile`


        :returns:   User, Usergroups and Organisations object
        :rtype:     Dict {user: :class:`~aquarium.items.user.User`, usergroups: [:class:`~aquarium.items.usergroup.Usergroup`], organisations: [:class:`~aquarium.items.organisation.Organisation`]}
        """
        return self.user.get_profile()

    def get_server_status(self):
        """
        Gets the server status.

        :returns:   The server status
        :rtype:     dictionary
        """
        result=self.do_request('GET', 'status')
        return result

    def upload_file(self, path=''):
        """
        Uploads a file on the server

        .. note::
            The file is just uploaded to Aquarium. The metadata are not saved on any item. Use :func:`~aquarium.item.Item.update_data` to save them on an item.
            You can also directly upload a file on an item with :func:`~aquarium.item.Item.upload_file`.

        :param      path:  The path of the file to upload
        :type       path:  string

        :returns:   The file metadata on Aquarium
        :rtype:     dictionary
        """
        logger.debug('Upload file : %s', path)
        files=dict(file=open(path, 'rb'))
        result = self.do_request('POST', 'upload', headers={'Content-Type': None}, files=files)
        files['file'].close()
        return result

    def query(self, meshql='', aliases={}):
        """
        Query entities

        .. tip::
            For better performances, we advice you to use the function :func:`~aquarium.item.Item.traverse`

        :param      meshql:        The meshql string
        :type       meshql:        string
        :param      aliases:       The aliases used in the meshql query
        :type       aliases:       dictionary

        :returns:   List of item, edge or VIEW used in the meshql query
        :rtype:     list
        """
        logger.debug('Send query : meshql : %s / aliases : %r',
                     meshql, aliases)
        data=dict(query=meshql, aliases=aliases)
        result=self.do_request('POST', 'query', data=json.dumps(data))
        return result

    def get_file(self, file_path):
        """
        Get stored file on Aquarium server

        :param      file_path:     The file path from item property (Exemple: `/files/file_id.jpg`)
        :type       file_path:     string

        :returns:   The file
        :rtype:     list
        """

        response = self.do_request('GET', file_path, decoding=False)
        return response.content
