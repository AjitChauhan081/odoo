# GearGuard – Backend

Backend interface for **GearGuard: The Ultimate Maintenance Tracker**, built as part of the **Odoo X Adani Hackathon**.

⚠️ **Important Note**  
The frontend depends completely on the backend APIs.  
👉 **You MUST run the backend first** before opening the frontend files.

---

## 📁 Frontend Files

The frontend consists of the following HTML files:

- `log_sign.html`  
  Login & Signup page (**entry point of the frontend**)

- `Dashboard.html`  
  Dashboard view  
- `Equipment.html`  
  Equipment management interface  
- `Manegment.html`  
  Maintenance request management  
- `Team.html`  
  Maintenance team management  
- `Workcenter.html`  
  Workcenter and maintenance operations view  
  
  *(Frontend by Manthon, API integration added by us)*

---

## 🚀 How to Run the Project (IMPORTANT)

### Step 1️⃣ Run the Backend First
The backend must be running before opening any frontend page.

Example:
```bash
uvicorn main:app --reload
```

## Step 2️⃣ Open the Frontend

After the backend is running:

1. Open `log_sign.html` in your browser  
2. Login / Signup  
3. Navigate through the application using the UI  

⚠️ **Important:**  
If the backend is **not running**, API-based features will **not work**.

---

## 🔗 Backend Dependency

The frontend uses APIs built with:

- **FastAPI**
- **SQLAlchemy**
- **Python**

All data such as:

- Equipment
- Maintenance Teams
- Maintenance Requests

is fetched from the backend APIs.

---

## 👥 Contribution Note

- **Frontend**: Created by **Manthan Vinzuda**
- **Backend** : Created by **Ajit Chauhan** & **Utsav Laheru**
- **API Integration & Backend Connection**: Added by our team

