<h1>
  Noxian Pool
</h1>
  A simple websites for players to join pool tournaments
<br></br>
  Created with:
  
  - Python 3.12 + Flask
  - Supabase

  Team members:

  - Pham Trung Hieu - 23021554: responsible for all database related CRUD functions
  - Nguyen Anh Duy - 23021502: logic implementations + front end development

<h2>
  Installation:
</h2>

Prerequisites:
  - python 3.12

Steps:
  - Create virtual environment:
      - On Linux:
      ```
      python -m venv env
      source envname/bin/activate
      pip install -r requirements.txt
      ```
    
      - On Windows:
      ```
      python -m venv env
      .\env\Scripts\activate.bat
      pip install -r requirements.txt
      ```
  - Add env file: Download the .env file from releases and paste it into the website's root folder
  - Run the website:
    ```
    python3 app.py
    ```
    When the website is running, open http://127.0.0.1:5000 on your browser to access it.
