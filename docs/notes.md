# Project notes



## Useful

### Watch logs on vps
sudo journalctl -u yourapp.service -f

### Vps pull and restart
git fetch
git checkout <branch-name>
git pull origin <branch-name>


sudo systemctl daemon-reexec        # 
sudo systemctl restart yourapp.service
sudo systemctl status yourapp.service
