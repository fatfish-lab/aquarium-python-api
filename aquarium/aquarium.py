# -*- coding: utf-8 -*-
import os
import mimetypes

from .auth import AquariumAuth
from .events import Events
from .item import Item
from .edge import Edge
from .tools import evaluate
from .items.bot import Bot
from .items.user import User
from .items.template import Template
from .items.project import Project
from .items.task import Task
from .items.shot import Shot
from .items.asset import Asset
from .items.usergroup import Usergroup
from .items.organisation import Organisation
from .items.playlist import Playlist
from .element import Element
from .events import Event
from .utils import Utils


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
    :param token: Specify the authentication token, to avoid :func:`~aquarium.aquarium.Aquarium.signin`
    :type token: string, optional
    :param api_version: Specify the API version you want to use (default : `v1`).
    :type api_version: string, optional
    :param domain: Specify the domain used for unauthenticated requests. Mainly for Aquarium Fatfish Lab dev or local Aquarium server without DNS
    :type domain: string, optional
    :param strict_dotmap: Specify if the dotmap should create new property dynamically (default : `False`). Set to `True` to have default Python behaviour like on Dict()
    :type strict_dotmap: boolean, optional

    :var token: Get the current token (populated after a first :func:`~aquarium.aquarium.Aquarium.signin`)
    :var events: Access to Events class
    :vartype events: :class:`~aquarium.events.Events`
    :var edge: Access to Edge class
    :vartype edge: :class:`~aquarium.edge.Edge`
    :var item: Access to Item class
    :vartype item: :class:`~aquarium.item.Item`
    :var asset: Access to Asset subclass
    :vartype asset: :class:`~aquarium.items.asset.Asset`
    :var playlist: Access to Playlist subclass
    :vartype playlist: :class:`~aquarium.items.playlist.Playlist`
    :var project: Access to Project subclass
    :vartype project: :class:`~aquarium.items.project.Project`
    :var shot: Access to Shot subclass
    :vartype shot: :class:`~aquarium.items.shot.Shot`
    :var task: Access to Task subclass
    :vartype task: :class:`~aquarium.items.task.Task`
    :var template: Access to Template subclass
    :vartype template: :class:`~aquarium.items.template.Template`
    :var bot: Access to Bot subclass
    :vartype bot: :class:`~aquarium.items.bot.Bot`
    :var user: Access to User subclass
    :vartype user: :class:`~aquarium.items.user.User`
    :var usergroup: Access to Usergroup subclass
    :vartype usergroup: :class:`~aquarium.items.usergroup.Usergroup`
    :var organisation: Access to Organisation subclass
    :vartype organisation: :class:`~aquarium.items.organisation.Organisation`
    :var utils: Access to Utils class
    :vartype utils: :class:`~aquarium.utils.Utils`
    """

    def __init__(self, api_url='', token=None, api_version='v1', domain=None, strict_dotmap=False):
        """
        Constructs a new instance.
        """
        # Session
        self.session=requests.Session()

        self.api_url=api_url
        self.api_version=api_version
        self.token=token
        self.domain=domain
        self.strict_dotmap=strict_dotmap

        # Classes
        self.events=Events(parent=self)
        self.element=Element(parent=self)
        self.item=Item(parent=self)
        self.edge=Edge(parent=self)
        self.utils=Utils()
        # SubClasses
        self.bot=Bot(parent=self)
        self.user=User(parent=self)
        self.usergroup=Usergroup(parent=self)
        self.organisation=Organisation(parent=self)
        self.template=Template(parent=self)
        self.project=Project(parent=self)
        self.playlist=Playlist(parent=self)
        self.task=Task(parent=self)
        self.shot=Shot(parent=self)
        self.asset=Asset(parent=self)
        self.event=Event(parent=self)

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

        stream=False
        if 'stream' in kwargs:
            stream=kwargs['stream']

        decoding=True
        if 'decoding' in kwargs:
            decoding=kwargs.pop('decoding')

        headers=None
        if 'headers' in kwargs:
            headers=kwargs.pop('headers')
            if headers is not None:
                headers.update(dict(authorization=token))

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
        response=self.session.request(typ, path, headers=headers, auth=AquariumAuth(self.token, self.domain), **kwargs)

        evaluate(response)
        if not stream:
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
                elif type=='Playlist':
                    cls=self.playlist
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
            #As Event
            elif id.split('/')[0]=='events':
                cls=self.event
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

    def ping (self):
        """
        Ping Aquarium server

        :returns: Ping response: pong
        :rtype:   string
        """
        ping = self.do_request('GET', 'ping', decoding=False)
        return ping.text

    def get_users (self):
        """
        Get all users

        :returns: List of all users
        :rtype:   List of :class:`~aquarium.items.user.User`
        """

        users = self.do_request('GET', 'users')

        users = [self.cast(user) for user in users]
        return users

    def create_user (self, email, name=None, aquarium_url=None):
        """
        Create a new user

        :param      email:  The email of the new user
        :type       email:  string
        :param      name:   The name of the new user
        :type       name:   string, optional
        :param      aquarium_url: The Aquarium Studio interface url. Useful if API url is not the same as Aquarium Studio interface.
        :type       aquarium_url: string, optional (default is api_url used during module initialisation)

        :returns:   User object
        :rtype:     :class:`~aquarium.items.user.User`
        """

        payload = dict(email=email)
        if name != None:
            payload['name'] = name

        headers = {
            'origin': aquarium_url or self.api_url
        }

        user = self.do_request(
            'POST', 'users', json=payload, headers=headers)

        user = self.cast(user)
        return user


    def forgot_password(self, email, aquarium_url=None):
        """
        Start forgot password procedure. User will receive an email to reset its password.

        :param      email:        Email of the user who forgot its password
        :type       email:        string
        :param      aquarium_url: The Aquarium Studio interface url. Useful if API url is not the same as Aquarium Studio interface.
        :type       aquarium_url: string, optional (default is api_url used during module initialisation)

        :returns: True or False
        :rtype: boolean
        """

        if (email is not None):
            data = {
                'email': email
            }
            headers = {
                'origin': aquarium_url or self.api_url
            }
            self.do_request(
            'POST', 'forgot', json=data, headers=headers)
            return True

    def upload_file(self, path='', encoded=False):
        """
        Uploads a file on the server

        .. note::
            The file is just uploaded to Aquarium. The metadata are not saved on any item. Use :func:`~aquarium.item.Item.update_data` to save them on an item.
            You can also directly upload a file on an item with :func:`~aquarium.item.Item.upload_file`.

        :param      path:  The path of the file to upload
        :type       path:  string
        :param      encoded:  If the video file is already encoded for the web and shouldn't be re-process by the server, optional
        :type       encoded:  boolean

        :returns:   The file metadata on Aquarium
        :rtype:     dictionary
        """
        logger.debug('Upload file : %s', path)

        file = open(path, 'rb')
        filename = os.path.basename(path)
        file_content_type = mimetypes.guess_type(filename)

        files=dict(file=(filename, file, file_content_type))

        headers = None
        if (encoded):
            headers = {
                "x-file-encoded": "true"
            }

        result = self.do_request('POST', 'upload', files=files, headers=headers)
        file.close()
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
        result=self.do_request('POST', 'query', json=data)
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
