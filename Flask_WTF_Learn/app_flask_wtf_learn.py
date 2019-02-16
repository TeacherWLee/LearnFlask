"""


__author__ = Li Wei (liw@sicnu.edu.cn)
"""
from flask import Flask, render_template, request
from flask_wtf import Form
from werkzeug.utils import secure_filename
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, EqualTo
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'niadxcnoylkadjf#$%65678^&*%#'
app.config['WTF_CSRF_ENABLED'] = False


class RegisterForm(Form):
    user_name = StringField(validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=4, max=20, message='用户名长度为4-20个字符')
    ])

    def validate_user_name(self, field):        # 自定义验证器
        pattern = '^[0-9a-zA-Z_]{1,}$'
        rst = re.findall(pattern, field.data)
        if not len(rst):
            raise ValidationError('用户名格式不合法，用户名由字母、数字和下划线组成')

    password = StringField(validators=[
                           InputRequired(message='密码不能为空'),
                           Length(min=6, max=20, message='密码长度在')
    ])

    confirm_password = StringField(validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=20, message='密码长度在'),
        EqualTo('password', message='Passwords must match')
    ])

    file = FileField()


@app.route('/')
def index():
    return render_template('forms.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = RegisterForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return '登录成功'
    else:
        return render_template('failure.html', form=form)


if __name__ == '__main__':
    app.run()


