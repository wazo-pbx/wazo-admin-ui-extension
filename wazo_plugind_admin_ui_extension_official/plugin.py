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

        register_listing_url('available_extension_incall', 'extension.ExtensionListingView:list_available_exten_incall')
        register_listing_url('available_extension_group', 'extension.ExtensionListingView:list_available_exten_group')
        register_listing_url('available_extension_user', 'extension.ExtensionListingView:list_available_exten_user')
        register_listing_url('available_extension_queue', 'extension.ExtensionListingView:list_available_exten_queue')
        register_listing_url('available_extension_conference', 'extension.ExtensionListingView:list_available_exten_conference')

        core.register_blueprint(extension)
