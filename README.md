# Homebrew-Scripts

Install tmux with:
```
sudo apt install tmux
```

Run this script on boot with:
```
tmux new-session -d -s homebrew-connection \; send-keys "python3 /home/pi/Homebrew-Scripts/connection.py" Enter
```
