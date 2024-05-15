# Playwright Web App Tester
 This program tests the functionality of https://staging.menuwise.com on adding recipes manually and adding recipes via URL using Playwright.

 ## Usage
 1. Requirements
 ```bash
Python >= 3.11
 ```

 2. Clone repository on local machine
 ```bash
git clone https://github.com/eliasezar27/test-menuwise.git
 ```

 3. Navigate to the root directory of the project and create environment.
 ```bash
 python -m venv venv
 ```

4. Install all dependencies from the `requirements.txt` file
```bash
pip install -r requirements.txt
```

5. Install Playwright
```bash
playwright install
```

6. Open git bash and activate environment
```bash
source venv/Scripts/activate <-for windows
source venv/bin/activate <- macOS
```

7. Create a `.env` file that stores the site credentials for logging in.
```bash
echo '' > .env
```

Open the file and populate the following:

```bash
SITE_USER_NAME=<username>
SITE_PASSWORD=<password>
```

8. Run program
```bash
python src/app.py
```