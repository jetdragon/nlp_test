#!/bin/bash
gunicorn -w1 -b0.0.0.0:5000 nlpServer:nlpServer
