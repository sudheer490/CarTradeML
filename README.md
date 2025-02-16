## AutoWise: The Intelligent Used Car Marketplace

**Description:** AutoWise is a cutting-edge used car marketplace that combines the power of machine learning with your car buying and selling needs. Experience a smarter and more efficient way to browse, buy, or sell used cars with our intelligent platform. AutoWise doesn't just connect car enthusiasts; it analyzes data to provide precise price predictions and offers personalized recommendations, ensuring you find the perfect vehicle. Welcome to the future of used car shopping with AutoWise !!

## Installation

in order to set up this project and install its dependencies, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```
2. Create a Virtual Environment (Optional but Recommended):

It's recommended to create a virtual environment to isolate the project's dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```
Install Dependencies:

Use pip to install the required packages listed in requirements.txt.

``` bash
pip install -r requirements.txt
```
## Dependencies
Listed are the dependencies needed.

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) (v4.12.2)
- [Flask](https://pypi.org/project/Flask/) (v3.0.0)
- [pandas](https://pypi.org/project/pandas/) (v2.1.1)
- [Pillow](https://pypi.org/project/Pillow/) (v10.0.1, v10.1.0)
- [psycopg2](https://pypi.org/project/psycopg2/) (v2.9.9)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) (v2.9.8)
- [Requests](https://pypi.org/project/requests/) (v2.31.0)
- [selenium](https://pypi.org/project/selenium/) (v4.14.0)
- [tqdm](https://pypi.org/project/tqdm/) (v4.66.1)

## Configuration Settings

Below are the configuration settings used in this project. You can modify these settings to match your environment and project requirements.
- You will have to make these changes in the ```app.conf``` file.

Move into the ```schema``` folder.
``` bash
cd ./app/schema
```
Then open ```app.conf``` in an editor and make the following changes.
```ini
[DEFAULT]
dbname = used_cars

[sql-prod]
bi_db = used_cars
host = localhost
user = your-user-name
dbname = used_cars
password = your-password
```
## Database Schema Setup
Before setting up the database schema for this project, ensure that you have PostgreSQL version 16 or later installed on your system. 
If you haven't already installed PostgreSQL, you can download and install it from the official PostgreSQL website: [Download PostgreSQL](https://www.postgresql.org/download/).

Once you have PostgreSQL installed, follow these steps:
To set up the database schema for this project, follow these steps:

1. **Create the Database:**

   First, create the database where the project's tables will be stored. You can do this using a SQL client or a command-line interface for your database system. Here's an example using PostgreSQL:

   ```sql
   CREATE DATABASE used_cars;
   ```
2. **Create Tables:**
  Run the SQL script tables.sql to create the necessary tables. You can use a SQL client or a command-line tool to execute the script. Here's an example using the PostgreSQL command-line tool:

```bash
psql -d used_cars -U your_username -a -f tables.sql
```
Make sure to replace your_username with your database username and provide any necessary authentication details.
