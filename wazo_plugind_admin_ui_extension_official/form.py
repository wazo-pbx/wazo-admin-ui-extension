# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import (SubmitField,
                            StringField,
                            SelectField)
from wtforms.validators import InputRequired

from wazo_admin_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = StringField('Extension', [InputRequired])
    context = SelectField('Context', [InputRequired], choices=[])
    submit = SubmitField('Submit')
