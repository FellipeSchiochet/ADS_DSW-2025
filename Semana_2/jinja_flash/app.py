from flask import Flask, render_template, request, redirect, url_for

app = Flask('__name__')

app.secret_key = 'Aqui_deve_ter_uma_chave_secreta'