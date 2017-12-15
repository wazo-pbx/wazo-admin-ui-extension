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
        form.context.choices = self._build_set_choices_context(form)
        return form

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            return []
        return [(extension.context.data, extension.context.data)]


class ExtensionListingView(LoginRequiredView):

    def list_available_exten_incall(self):
        return self._list_available_exten(context_range='incall_ranges')

    def list_available_exten_group(self):
        return self._list_available_exten(context_range='group_ranges')

    def list_available_exten_user(self):
        return self._list_available_exten(context_range='user_ranges')

    def list_available_exten_queue(self):
        return self._list_available_exten(context_range='queue_ranges')

    def list_available_exten_conference(self):
        return self._list_available_exten(context_range='conference_room_ranges')

    def _list_available_exten(self, context_range):
        search = request.args.get('term') or ''
        context = request.args.get('context')
        if not context:
            return jsonify({'results': []})

        context = self.service.get_context(context)
        if not context:
            return jsonify({'results': []})

        all_extens = set()
        for ressource_range in context[context_range]:
            try:
                start = int(ressource_range['start'])
                end = int(ressource_range['end']) + 1
            except ValueError:
                continue

            if end - start > MAX_POSSIBILITIES:
                end = start + MAX_POSSIBILITIES

            # TODO benchmark to improve this
            for v in range(start, end):
                if not search or search in str(v):
                    if context_range == 'incall_ranges':
                        all_extens.add(str(v).zfill(ressource_range['did_length']))
                    else:
                        all_extens.add(str(v))

        if not all_extens:
            return jsonify({'results': []})

        used_extens = set([])
        for extension in self.service.list(search=search, context=context['name'])['items']:
            if search and search not in extension['exten']:
                continue

            used_extens.add(extension['exten'])

        valid_extens = all_extens - used_extens
        valid_extens = sorted(valid_extens)

        results = [{'id': exten, 'text': exten} for exten in valid_extens]
        return jsonify({'results': results})
