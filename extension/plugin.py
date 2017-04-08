# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url

from .service import ExtensionService
from .view import ExtensionListingView

extension = create_blueprint('extension', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        ExtensionListingView.service = ExtensionService()
        ExtensionListingView.register(extension, route_base='/extensions_listing')

        register_listing_url('extension', 'extension.ExtensionListingView:list_json')

        core.register_blueprint(extension)
