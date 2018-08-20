# Homebrew-Scripts

## Run on boot

Install tmux with:
```
sudo apt install tmux
```

Add this line to ```/etc/rc.local``` before ```exit 0```:
```
tmux new-session -d -s homebrew-connection \; send-keys "python3 /home/pi/Homebrew-Scripts/connection.py" Enter
```
