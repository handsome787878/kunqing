from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
)
from email_validator import validate_email, EmailNotValidError


class RegisterForm(FlaskForm):
    student_id = StringField("学号", validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        "确认密码",
        validators=[DataRequired(), EqualTo("password", message="两次密码不一致")],
    )
    captcha = StringField("验证码", validators=[DataRequired(), Length(min=4, max=6)])
    submit = SubmitField("注册")

    def validate_email(self, field):
        try:
            validate_email(field.data)
        except EmailNotValidError as e:
            raise ValidationError(str(e))


class LoginForm(FlaskForm):
    account = StringField("学号或邮箱", validators=[DataRequired(), Length(min=4, max=120)])
    password = PasswordField("密码", validators=[DataRequired()])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")


class ProfileForm(FlaskForm):
    real_name = StringField("姓名", validators=[Length(max=50)])
    college = StringField("学院", validators=[Length(max=100)])
    major = StringField("专业", validators=[Length(max=100)])
    grade = StringField("年级", validators=[Length(max=20)])
    phone = StringField("电话", validators=[Length(max=20)])
    submit = SubmitField("保存")


class PasswordResetForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    captcha = StringField("验证码", validators=[DataRequired(), Length(min=4, max=6)])
    new_password = PasswordField("新密码", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        "确认密码",
        validators=[DataRequired(), EqualTo("new_password", message="两次密码不一致")],
    )
    submit = SubmitField("重置密码")