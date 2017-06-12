# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_destination_form, register_listing_url

from .form import ExtensionDestinationForm
from .service import ExtensionService
from .view import ExtensionView, ExtensionListingView


extension = create_blueprint('extension', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        ExtensionView.service = ExtensionService()
        ExtensionView.register(extension, route_base='/extensions')
        register_flaskview(extension, ExtensionView)

        ExtensionListingView.service = ExtensionService()
        ExtensionListingView.register(extension, route_base='/extensions_listing')

        register_destination_form('extension', 'Extension', ExtensionDestinationForm)

        register_listing_url('available_extension', 'extension.ExtensionListingView:list_available_exten')

        core.register_blueprint(extension)
