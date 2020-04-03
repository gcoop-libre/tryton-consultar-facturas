# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError
from . import captcha as captcha_object

class ConsultaForm(FlaskForm):

    nro_cliente = StringField("Cliente", [DataRequired(), Length(1,11)])
    identificador = StringField("CUIT", [DataRequired(), Length(1,11)])
    captcha = StringField("Captcha", [DataRequired()])

    def validate_captcha(form, field):
        if not captcha_object.validate():
            raise ValidationError("El captcha ingresado es incorrecto")
