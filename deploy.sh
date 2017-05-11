echo "Copying files"

scp ./*.py pi@$1:/home/pi/Python/KnightSpider-MainFrame/

ssh pi@$1 "cd ~/Python/KnightSpider-MainFrame/ && python3 main.py"
