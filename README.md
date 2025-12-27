# Odoo X Adani Hackathon

## GearGuard: The Ultimate Maintenance Tracker

A backend-driven maintenance management system built for the **Odoo X Adani Hackathon**, using **Python**, **SQLAlchemy**, and **FastAPI**.

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM for database management
- **PostgreSQL / SQLite** (configurable)

---

## 🎯 Objective

Develop a **maintenance management system** that allows a company to:

- Track its assets (machines, vehicles, computers)
- Manage maintenance requests for those assets
- Assign responsibility clearly between **Equipment**, **Maintenance Teams**, and **Requests**

---

## 🧠 Core Philosophy

The system must seamlessly connect:

- **Equipment** → *What is broken*
- **Maintenance Teams** → *Who fixes it*
- **Maintenance Requests** → *The work to be done*

This tight integration ensures traceability, accountability, and efficient maintenance workflows.

---

## A. Equipment

The system acts as a **central database** for all company assets.

### 🔍 Equipment Tracking
Equipment can be tracked and filtered using **search or group-by** options:

- **By Department**  
  Example: A CNC Machine belongs to the *Production* department.
- **By Employee**  
  Example: A Laptop belongs to a specific employee.

### 👷 Responsibility
- Each equipment is linked to a **dedicated Maintenance Team**
- A technician is assigned **by default**

### 📌 Key Fields
- Equipment Name
- Serial Number
- Purchase Date
- Warranty Information
- Location (physical location of the asset)

---

## B. Maintenance Team

The system supports **multiple specialized teams**.

### 👥 Team Structure
- **Team Name**  
  Examples: Mechanics, Electricians, IT Support
- **Team Member Name**  
  Technicians linked to a team

### 🔄 Workflow Logic
- When a request is created for a specific team, **only members of that team** can pick it up.

---

## C. Maintenance Request

This is the **transactional core** of the system, handling the lifecycle of repair jobs.

### 🧾 Request Types
- **Corrective** – Unplanned repair (Breakdown)
- **Preventive** – Planned maintenance (Routine Checkup)

### 📌 Key Fields
- Subject (e.g., *Leaking Oil*)
- Equipment (affected machine)
- Scheduled Date
- Duration (hours spent on repair)

---

## 🔁 Functional Workflow

### Flow 1: The Breakdown (Corrective Maintenance)

1. **Request Creation**  
   Any user can create a maintenance request.
2. **Auto-Fill Logic**  
   When an Equipment is selected:
   - Equipment category is fetched automatically
   - Maintenance Team is auto-filled from the equipment record
3. **Initial State**  
   Request starts in **New**
4. **Assignment**  
   A manager or technician assigns themselves
5. **Execution**  
   Status moves to **In Progress**
6. **Completion**  
   Technician records **Duration** and moves status to **Repaired**

---

### Flow 2: The Routine Checkup (Preventive Maintenance)

1. **Scheduling**  
   Manager creates a request with type **Preventive**
2. **Date Setting**  
   A Scheduled Date is assigned (e.g., *Next Monday*)
3. **Calendar Visibility**  
   The request appears in **Calendar View** for technicians

---

## 🧩 User Interface & Views Requirements

### 1️⃣ Maintenance Kanban Board
Primary workspace for technicians.

- **Group By Stages**:
  - New
  - In Progress
  - Repaired
  - Scrap
- **Drag & Drop**  
  Users can move requests between stages

### 🎨 Visual Indicators
- Technician avatar on request card
- Overdue requests highlighted with red indicator

---

### 2️⃣ Calendar View
- Displays all **Preventive** maintenance requests
- Allows users to click a date to schedule new requests

---

### 3️⃣ Pivot / Graph Report (Optional)
- Number of requests per:
  - Maintenance Team
  - Equipment Category

---

## 🤖 Required Automation & Smart Features

### 🔘 Smart Buttons
- **Maintenance Button** on Equipment form
- Opens a list of maintenance requests related to that equipment
- Displays a **badge count** of open requests

### 🗑️ Scrap Logic
- If a request is moved to **Scrap**:
  - Equipment is logically marked as unusable
  - A flag or note is logged for traceability

---

## 🚀 Summary

**GearGuard** transforms basic maintenance tracking into a **smart, Odoo-like module** by combining:

- Structured asset management
- Team-based responsibility
- Automated workflows
- Visual and calendar-based planning

---

## 👨‍💻 Hackathon Project

Built as part of the **Odoo X Adani Hackathon**  
Focused on **clean backend design**, **business logic**, and **scalable architecture**.
