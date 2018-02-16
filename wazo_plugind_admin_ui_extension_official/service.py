# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService
from wazo_admin_ui.helpers.confd import confd


class ExtensionService(BaseConfdService):
    resource_confd = 'extensions'

    def get_context(self, context):
        contexts = confd.contexts.list(name=context)['items']
        for context in contexts:
            return context
        return None


class ExtensionFeaturesService(BaseConfdService):
    resource_confd = 'extensions_features'

    def update_extension_features(self, resources):
        for resource in resources:
            self.update(resource)