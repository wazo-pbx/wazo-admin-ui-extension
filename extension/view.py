# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import jsonify, request
from wazo_admin_ui.helpers.classful import LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response


class ExtensionListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        context = request.args.get('context')
        if context:
            params['context'] = context

        extensions = self.service.list(**params)
        results = [{'id': extension['exten'], 'text': extension['exten']} for extension in extensions['items']]
        return jsonify(build_select2_response(results, extensions['total'], params))
