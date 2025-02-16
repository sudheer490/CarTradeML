# 🚗 **GearUp : The Intelligent Used Car Marketplace** 🚀  

![GearUp  Banner](https://your-image-url.com/banner.png) <!-- Replace with a real banner image URL -->

## **📌 Overview**
**GearUp ** is a cutting-edge **AI-powered** used car marketplace that enhances your buying and selling experience with **data-driven insights**. Our platform utilizes **machine learning algorithms** to predict resale values, recommend the best deals, and personalize the search process—making it easier than ever to **find the perfect vehicle** at the right price.

✅ **Key Features:**
- **Smart Price Prediction**: Get accurate car valuations using advanced machine learning models.  
- **Personalized Car Recommendations**: Find the best vehicles based on your preferences and market trends.  
- **Seamless Car Selling**: Get an instant price estimate for your car in **under 2 minutes**.  
- **Intelligent Search & Filters**: Refine your search based on brand, model, features, and price.  

🎥 **Watch the Demo:**  
🔗 [Click here to watch](https://www.youtube.com/watch?v=Ltb2npcErZ8)

[![Watch the Video](https://img.youtube.com/vi/Ltb2npcErZ8/maxresdefault.jpg)](https://www.youtube.com/watch?v=Ltb2npcErZ8)

---

## **🛠️ Installation & Setup**
To set up **GearUp ** on your local machine, follow these steps:

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/GearUp .git
cd GearUp 
```

### **2️⃣ Create a Virtual Environment** (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Database Settings**
- Move into the `schema` folder:
  ```bash
  cd ./app/schema
  ```
- Open `app.conf` and update your **PostgreSQL** credentials:
  ```ini
  [DEFAULT]
  dbname = used_cars

  [sql-prod]
  bi_db = used_cars
  host = localhost
  user = your-username
  dbname = used_cars
  password = your-password
  ```

### **5️⃣ Setup the Database**
Before proceeding, ensure you have **PostgreSQL 16+** installed.  
[Download PostgreSQL](https://www.postgresql.org/download/) if needed.

- **Create Database**:
  ```sql
  CREATE DATABASE used_cars;
  ```

- **Import Tables**:
  ```bash
  psql -d used_cars -U your_username -a -f tables.sql
  ```
  *(Replace `your_username` with your actual PostgreSQL username.)*

---

## **📦 Dependencies**
These are the required dependencies for **GearUp **:

| Package          | Version  | Description |
|-----------------|---------|-------------|
| Flask           | `3.0.0` | Backend framework |
| pandas          | `2.1.1` | Data processing |
| beautifulsoup4  | `4.12.2` | Web scraping |
| selenium        | `4.14.0` | Browser automation |
| psycopg2-binary | `2.9.8` | PostgreSQL database driver |
| Pillow          | `10.1.0` | Image processing |

Install them using:
```bash
pip install -r requirements.txt
```

---

## **🚀 Running the Application**
Once the setup is complete, launch **GearUp ** by running:

```bash
python app.py
```

Now, open your browser and navigate to:
```
http://127.0.0.1:5000
```

🚀 **You're all set! Start exploring the future of used car shopping with GearUp !** 🚗

---
