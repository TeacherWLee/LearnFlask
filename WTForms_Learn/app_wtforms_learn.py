"""


__author__ = Li Wei (liw@sicnu.edu.cn)
"""
from flask import Flask, render_template, request
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, EqualTo
import re

app = Flask(__name__)
app.config['DEBUG'] = True


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


@app.route('/')
def index():
    return render_template('forms.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = RegisterForm(request.form)
    if form.validate():
        return '登录成功'
    else:
        return render_template('failure.html', message=form.errors)


if __name__ == '__main__':
    app.run()


