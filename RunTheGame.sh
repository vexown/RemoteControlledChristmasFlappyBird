#!/bin/bash

pgzrun flappybird/flappybird.py

exit_code=$?

# Check if the exit code is 7 and call AfterWinScript accordingly (basically call this only if you win at flappy bird)
if [ $exit_code -eq 7 ]; then
    python3 AfterWinScript.py
fi