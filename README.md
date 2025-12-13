# Invento  
**Invento** is a backend inventory‑management system built with Django REST Framework (DRF).
It uses JWT authentication, background tasks with Celery for mailing, and enables tracking stock in/out,
managing suppliers & customers, and includes a dashboard for analytics.
---

## 🧩 Features  
- User authentication via Simple JWT  
- CRUD APIs for products, suppliers, customers  
- Stock movement: inbound (stock‑in) and outbound (stock‑out) operations  
- Dashboard analytics: insights about inventory, suppliers, customers  
- Modular Django app structure (core, products, main_folder etc)  
---

## 🚀 Technology Stack  
- Python  
- Django / Django REST Framework  
- Simple JWT for token‑based auth   
- PostgreSQL for persistent storage  
---

## 🔧 Getting Started  
### Prerequisites  
- Python (e.g., 3.10+)  
- MySQL (or configured database)    
- Git  

### Installation  
1. Clone the repo:  
   ```bash
   git clone https://github.com/Niraj-commits/Invento.git
   cd Invento
   ```  
2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Unix/macOS
   # or venv\Scripts\activate on Windows
   ```  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Configure your `.env` / `settings.py`:  
   - Set database credentials (PostgreSQL)    
5. Run migrations:  
   ```bash
   python manage.py migrate
   ```  
6. (Optional) Create a superuser:  
   ```bash
   python manage.py createsuperuser
   ```  
7. Run the web server:  
   ```bash
   python manage.py runserver
   ```  

## 🎯 Usage  
- Register or login as a user.  
- Use JWT tokens to access protected endpoints.  
- Create suppliers and customers.  
- Add products and manage stock‑in/out entries.  
- Visit dashboard endpoints to view analytics (e.g., total stock, low stock alerts, supplier/customer stats).  

## 📄 License    
No license – all rights reserved_

---

## 📬 Contact  
Created by **Niraj**.  
Feel free to open issues or pull requests on this repository if you have suggestions or spot bugs.
