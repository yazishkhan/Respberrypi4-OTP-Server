# 🕹️ Reapberrypi-OTP-server 🕹️

#### Building an OTP server which can able to implement in Real-time websites.

### 🧠 Advantages
- If you are building an web application which needs an OTP login. You can able to integrate it.
- Easy to set-up.
- Just implement UI and use this 

### 🤖 Hardware
- Raspberry Pi 4 

- SD card with pi OS installed 64bit.

- SIM800L GSM Module (expects 3.7V–4.4V)

- I2C Logic Level Converter (to safely connect SIM800L to Pi GPIOs)

- External power source for SIM800L (VERY important)

- SIM card with SMS balance
<br/>

### 🌐 Softwares 
`Python3` Latest version of python using with raspberry pi.
` Flask ` The easiest framework to make API has support of `RestApi` and `FetchApi`.
`pyserial` For UART communication with SIM800L
<br/>

### 🔌 Circuit Wiring 

    🔴  Note :- 
        External power supply NEEDED for powiring SIM module not works with pi's supply
        Connect ground's (-) of Pi4,SIM800L and I2C logic level converter to external powerfully's (-)ve.
<br/>

| SIM800L Pin | Connects To              | Description                        |
| ----------- | ------------------------ | ---------------------------------- |
| **VCC**     | External 4V Power (+)    | Not Pi 5V – use a stable 4V source |
| **GND**     | Pi GND **and** Power GND | Common ground is critical          |
| **TX**      | **LV1** of Level Shifter | SIM800L → Pi (data IN to Pi)       |
| **RX**      | **LV2** of Level Shifter | Pi → SIM800L (data OUT from Pi)    |


| Level Converter | Connects To               |
| --------------- | ------------------------- |
| **LV**          | Pi 3.3V                   |
| **HV**          | SIM800L VCC (4V)          |
| **GND**         | Shared GND (Pi & SIM800L) |
| **LV1**         | Pi GPIO15 (UART RX)       |
| **LV2**         | Pi GPIO14 (UART TX)       |
| **HV1**         | SIM800L TX                |
| **HV2**         | SIM800L RX                |

<br/>

### 🔢 Block Circuit Diagram

````
+-----------+            +--------------------+           +--------------+
| Raspberry |  GPIO 8 TX | LV2 →     HV2      | RX ←      |  SIM800L     |
|   Pi 4    | ---------->|   Level Converter  | --------> |              |
|           |  GPIO10 RX | LV1 ←     HV1      | TX ←      |              |
|           |            +--------------------+           |              |
|           |     3.3V → LV                               |              |
|           |     GND  → GND     HV ← 4V (from external)  |              |
+-----------+                                          VCC| ← 4V Power   |
                                                       GND| ← GND        | 
                                                          +--------------+
````
<br/>

 ![Image](https://github.com/user-attachments/assets/5d2b13be-121b-42ea-97e8-3f1c685d54c2)

### 🔧 Software Setup on Raspberry Pi
:red_circle: First Clone this repo
1. Enable UART on Pi
    ````bash
    sudo raspi-config
    ````
- Go to Interface Options > Serial

- Login shell over serial? → No

- Enable serial port hardware? → Yes 

- Then Reboot 

    ```` bash
    sudo reboot 
    ````

2. Install Python Dependencies
- Updating and installing python
    ````bash
    sudo apt update
    sudo apt install python3-pip
    ````
- Installing `Flask` and `pyserial`
    ````bash
    sudo apt install python3-flask python3-serial -y
    ````
3. Insert the Sim card in SIM800L module (with SMS recharge).
<br/>

4. To check if module and wires are connected properly
- locate on directory where the repo is cloned 
- run the script called `sim_800l.py`
    ````bash
    sudo python3 sim_800l.py
    ````
5. To check SIM800l module strength and connectivity run the script called `sim_check.py`
    ````bash
    sudo sim_check.py
    ````
6. :red_circle: Note If SIM800l module is troubling to connect to Sim card network.
- Try to put the SIM800l module in area where it has connectivity.
- Check the wiring properly.
- Make sure all the wires are connected properly it may not be damage.
- Connect the antina properly.
- Then if it is not able to connect.
-- Get an `16v 220uf capacitor`
-- And connect to the Tantalum capacitor present on SIM800l module. 
![implementation](https://github.com/user-attachments/assets/3ff007a9-caf4-41b1-b1e8-4dfab6cf0f90)
<br/>
##### :red_circle: Then run the scripts it's definitely  going to work.
<br/>

### :rocket: Running the Flask server to Test the OTP is able to send.
1. Run this command by using `otp_server.py` it runs a Flask server in detached mode and store all logs inside the output.log file.
    ````bash 
    nohup python3 otp_server.py > output.log 2>&1 &
    ````
- After entering this command it gives an process ID it helps to stop flask server.(**Only run when you want to stop flask server**)
    ````bash 
    kill <process-id>
    ````
2. Then Enter this command and replace the IP in which flask server is running and Enter the mobile not no which you want to send OTP.
    ````bash
    curl -X POST http://192.168.0.100:5000/send_otp \
      -H "Content-Type: application/json" \
      -d '{"phone": "+9198769xxxx"}'
    ````
- Replace the IP `192.168.0.100` with your Pi's IP.
- If you wanted to know your pi's IP run these command.
    ````bash
    ifconfig
    ````
- Copy the IP addr and replace with the curl command.
- Also replace the mobile number `+91 98769xxxx` on which you want to send OTP;
<br/>

### 📥 Final implementation of Database and Validation

> #### 🧱 1. Install Required Packages.
- Run this command to update pi and install mysql, pymysql.
    ````bash
    sudo apt update
    sudo apt install mariadb-server
    sudo apt install python3-pymysql
    ````
> #### 📥 2. Setting-up Mysql DB.
- Configuring Mysql.
    ````bash
    mysql -u root -p 
    ````
    - Then it asks for password enter it.
    - At first it through Error like this. <br/>
    ![Image](https://github.com/user-attachments/assets/27291085-30a2-4062-a3b7-6a45245cb347) 
    -  The issue is most likely that the password was not actually set for the root user. SOLVED by this!
    1. Enter MariaDB shell as root:

        ````bash
        sudo mysql
        ````
    2. Set the password for root user.
        - Copy on normal text editor and replace `741593` with password you want to give for Mysql login.
        - Then Copy and pest on SQL terminal.
        ````sql
        SET PASSWORD FOR 'root'@'localhost' = PASSWORD('741593');
        FLUSH PRIVILEGES;
        ````
        :red_circle: Note this password we also need to replace in python file.
    3. Exit.
        ````sql
        EXIT;
        ````
    4. Restart MariaDB 
        ````bash
        sudo systemctl restart mariadb
        ````
    5. Now test login
        ````bash
        mysql -u root -p
        ````
        **It has been finally solved.**
- Creating Database.
    1. Run these Script to create database. (On Mysql terminal).
        
        ````sql 
        source /home/pi/Downloads/db.sql
        ````
    - replace the path `/home/pi/Downloads/db.sql` As per repo you cloned on your device.
    - It will automatically create database.
          
- Linking Database to python code.
    1. Open the file called `flask-otp-DB.py`.
        ````bash
        nano flask-otp-DB.py
        ````
    2. Locate for this section and replace the `password` which we set for MYSQL login.
        ![Image](https://github.com/user-attachments/assets/e9c53f7c-4af8-479f-9aeb-00f3d180093e)
    
    
        **And Everything is Done 💥**
> #### ✅ 3. Running OTP server With DB and OTP-Validation.

- Running Flask Server.
    ````bash
    nohup python3 flask-otp-DB.py > flask.log 2>&1 &
    ````
    - After entering this command it gives an process ID it helps to stop flask server by doing.(**Only run when you want to stop flask server**)
    ````bash 
    kill <process-id>
    ````
    - `nohup`: Prevents the process from stopping when you close SSH

    - `flask.log 2>&1`: Saves output & errors to `flask.log`

    - `&`: Runs in background
      
- 🔍 To check if it's running:
    ````bash
    ps aux | grep flask-otp-DB.py
    ````
    <br/>
- Feeding data to Test OTP is sending.
    ````bash
    curl -X POST http://<Your-pi-ip>:5000/send_otp \
    -H "Content-Type: application/json" \
    -d '{"phone": "+919876xxxx"}'
    ````
    - Replace `Your-pi-ip` with actual IP address of your pi.
    - Replace mobile no `+919876xxxx` to on which you want to send OTP.
    - By entering it, sends an OTP to your mobile.
- Validating received OTP.
    ````bash

    
    curl -X POST http://<pi-ip>:5000/verify_otp \
    -H "Content-Type: application/json" \
    -d '{"phone": "+919876xxxx", "otp": "123456"}'
    ````
    - Replace `Your-pi-ip` with actual IP address of your pi.
    - Replace the mobile no which you received an OTP
    - And also replace `123456` with the received OTP.
   

#### 📝 Points to be note
- ###### Implement a Frontend with API Endpoint and BOOOOM ready to go with the functionality of OTP login on your website.
- This project dose not contains any Encryption.
- Do not store OTP's in DB like plain test.
- Whenever using this in production level add encryption and implement UI by making changes in Flask code.

### Made by. [Yazish Khan](https://www.linkedin.com/in/yazish-khan-3634752b7?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
