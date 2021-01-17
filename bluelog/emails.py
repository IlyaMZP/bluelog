# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from bluelog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = current_app.config['BLUELOG_DOMAIN_NAME'] + url_for('blog.show_post', post_id=post.id) + '#comments'
    send_mail(subject='New comment', to=current_app.config['BLUELOG_ADMIN_EMAIL'],
              html='<p>New comment in post <i>%s</i>, click the link below to check:</p>'
                   '<p><a href="http://%s">%s</a></P>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    if comment.email:
        post_url = current_app.config['BLUELOG_DOMAIN_NAME'] + url_for('blog.show_post', post_id=comment.post_id) + '#comments'
        send_mail(subject='New reply', to=comment.email,
                  html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                       '<p><a href="http://%s">%s</a></p>'
                       '<p><a href="http://%s/admin/unsubscribe/%s">Unsubscribe</a></p>'
                       '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                       % (comment.post.title, post_url, post_url, current_app.config['BLUELOG_DOMAIN_NAME'], comment.email))
