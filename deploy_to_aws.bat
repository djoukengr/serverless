@echo off
call npm init -f
call npm install --save-prod serverless-wsgi serverless-python-requirements
serverless deploy
@pause
