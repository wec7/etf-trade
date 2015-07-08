# etf-trade
ETF pre-trade analysis

### Installation Guide

##### System Requirements
Make sure your system meets these requirements:
  - Operating system: MacOS 10.7 - 10.10 (it has been tested successfully on these)
  - RAM: 2GB.
  - Disk space: 2GB

##### Step 1: Install Command Line Tools
  - Open terminal, type “xcode-select --install” in terminal (without quotes)
  - A pop-up windows will appear asking you about install tools, choose install tools, wait install to finish
  
##### Step 2: Install Homebrew
  - Copy paste following command to the terminal, and press Enter.
  
  ```
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```

##### Step 3: Install Python and its modules
  - Copy paste following commands to the terminal, and press Enter.
  
  ```
  brew install python
  
  pip install pandas
  pip install datetime
  pip install apscheduler
  ```

### Running Guide

##### One-time Run:

 - Go to `etf-trade` directory and run the python script `main.py`.

 ```
 cd ~/etf-trade
 python main.py
 ```
 
 - Type in your gmail address and password.
 
 ```
 Your Gmail address: xxx.xxx.xxx@gmail.com
 Password: xxxxxxxx
 ```
 
##### Automatic Run:

  - Go to `etf-trade` directory and run the python script `scheduler.py`.

  ```
  cd ~/etf-trade
  python scheduler.py
  ```

  Never close it, it will send you the suggested ETF csv file at 5pm every business day.
