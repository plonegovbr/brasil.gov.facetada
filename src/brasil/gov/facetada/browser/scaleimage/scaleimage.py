# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
import cgi
import json


class ScaleImage(BrowserView):
    """
    Returns JSON with resized image information
    """

    def update(self):
        """Parse params
        Possible params:
        - `path`: One ore more image paths separated by ';'
        - `uid`: One ore more image uids separated by ';'
        - `scale`: Plone registered scale to use
        - `width`: Custom width to use
        - `height`: Custom height to use
        """
        self.params = self.request.form
        self.path = self.params.get('path', [])
        if self.path:
            self.path = self.path.split(';')
        self.uid = self.params.get('uid', [])
        if self.uid:
            self.uid = self.uid.split(';')
        self.scale = self.params.get('scale', None)
        self.width = self.params.get('width', None)
        self.height = self.params.get('height', None)

    def _to_json(self, data):
        """Return json from DICT
        Arguments:
        - `data`: DICT with data to return
        """
        pretty = json.dumps(data,
                            sort_keys=True,
                            indent=4)
        minutes = 20
        seconds = minutes * 60
        self.request.response.setHeader('Cache-Control',
                                        's-maxage=%d' % int(seconds))
        self.request.response.setHeader('Access-Control-Allow-Origin',
                                        '*')
        self.request.response.setHeader('Content-Type',
                                        'application/json')
        return pretty

    def _get_image_data(self, image):
        """Return dict with image data
        """
        image_data = {}
        scales = image.restrictedTraverse('@@images')
        thumb = None
        if self.scale:
            thumb = scales.scale('image',
                                 self.scale)
        elif self.width and self.height:
            thumb = scales.scale('image',
                                 width=self.width,
                                 height=self.height)
        if thumb:
            image_data['path'] = '/'.join(image.getPhysicalPath())
            image_data['description'] = cgi.escape(str(image.Description()))
            image_data['height'] = thumb.height
            image_data['mimetype'] = thumb.mimetype
            image_data['scale'] = self.scale
            image_data['tag'] = cgi.escape(str(thumb.tag()))
            image_data['title'] = cgi.escape(str(image.Title()))
            image_data['uid'] = thumb.uid
            image_data['url'] = thumb.url
            image_data['width'] = thumb.width
        return image_data

    def render(self):
        """Return scaled image data for use with AJAX request"""
        data = []

        if self.path or self.uid:
            for path in self.path:
                image = api.content.get(path=path)
                if image:
                    image_data = self._get_image_data(image)
                    data.append(image_data)
            for uid in self.uid:
                image = api.content.get(UID=uid)
                if image:
                    image_data = self._get_image_data(image)
                    data.append(image_data)
        else:
            image_data = self._get_image_data(self.context)
            data.append(image_data)
        if len(data) == 1:
            data = data[0]
        return self._to_json(data)

    def __call__(self):
        self.update()
        return self.render()
