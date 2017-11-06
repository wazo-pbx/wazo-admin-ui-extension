# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from .form import ExtensionForm

MAX_POSSIBILITIES = 1000


class ExtensionView(BaseView):

    form = ExtensionForm
    resource = 'extension'

    @classy_menu_item('.advanced', 'Advanced', order=9, icon="gears")
    @classy_menu_item('.advanced.extensions', 'Extensions', order=1, icon="tty")
    def index(self):
        return super(ExtensionView, self).index()

    def _populate_form(self, form):
        form.context.choices = self._build_setted_choices_context(form)
        return form

    def _build_setted_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            return []
        return [(extension.context.data, extension.context.data)]


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
                end = int(user_range['end']) + 1
            except ValueError:
                continue

            if end - start > MAX_POSSIBILITIES:
                continue

            values = [v for v in range(start, end) if not search or search in str(v)]
            all_extens.update(values)

        if not all_extens:
            return jsonify({'results': []})

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
