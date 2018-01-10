# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (SubmitField,
                            StringField,
                            SelectField)
from wtforms.validators import InputRequired

from wazo_admin_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = StringField(l_('Extension'), [InputRequired])
    context = SelectField(l_('Context'), [InputRequired], choices=[])
    submit = SubmitField(l_('Submit'))


class ExtensionDestinationForm(BaseForm):
    exten = StringField(l_('Extension'), [InputRequired])
    context = StringField(l_('Context'), [InputRequired])
