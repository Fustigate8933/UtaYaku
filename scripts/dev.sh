#!/bin/bash
pnpm nuxt dev &
pnpm fastapi dev backend/hugchat_main.py
wait

