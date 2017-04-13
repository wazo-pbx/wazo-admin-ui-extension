# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import jsonify, request
from wazo_admin_ui.helpers.classful import LoginRequiredView


class ExtensionListingView(LoginRequiredView):

    def list_available_exten(self):
        search = request.args.get('term') or ''
        context = request.args.get('context')
        if not context:
            return jsonify({'results': []})

        context = self.service.get_context(context)
        if not context:
            return jsonify({'results': []})

        all_extens = set()
        for user_range in context['user_ranges']:
            try:
                start = int(user_range['start'])
                end = int(user_range['end'])
            except ValueError:
                continue

            values = [v for v in xrange(start, end+1) if not search or search in unicode(v)]
            all_extens.update(values)

        used_extens = set([])
        for extension in self.service.list(search=search)['items']:
            if search and search not in extension['exten']:
                continue
            try:
                used_exten = int(extension['exten'])
            except ValueError:
                continue
            used_extens.add(used_exten)

        valid_extens = all_extens - used_extens
        valid_extens = list(valid_extens)
        valid_extens.sort()

        results = [{'id': exten, 'text': exten} for exten in valid_extens]
        return jsonify({'results': results})
