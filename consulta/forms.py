#! -*- coding: utf8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class ConsultaForm(FlaskForm):

    nro_cliente = StringField("Cliente", [DataRequired(), Length(1,11)])
    identificador = StringField("CUIT", [DataRequired(), Length(1,11)])
