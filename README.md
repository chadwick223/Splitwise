<h1>Demo  (https://drive.google.com/file/d/1TOuUUazncxMub2X1lsrQMdsRIAZkXq_o/view?usp=sharing)</h1>


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with that out of the way let's start with lld diagram of this Epense splitting application (web app actually since i do not know app dev namely flutter n all)

<h2>LLD are devided into three parts </h2>

<h3>lld </h3> https://drive.google.com/file/d/1vIieP9XEVc0OXutJx0ZU2cumUPhybV_Z/view?usp=sharing
<h3>lld part 2</h3> https://drive.google.com/file/d/1oBlnckwm8X1bmKDXsTe4OqSrW5fAnSbL/view?usp=sharing
<h3>lld part 3</h3>https://drive.google.com/file/d/1dLcPETJEP-B91UHmabAHCIxYgWUU3GlD/view?usp=sharing


<h1> Models desgin (for database )</h1>
https://drive.google.com/file/d/1rVwd8rXeIj8JjgW5_Y3YhyRWC3wT_Gge/view?usp=sharing
<h3>The database used is SQLITE  </h3>

<h1> Form diagram for user input </h1>
https://drive.google.com/file/d/1tqXrqU_iM5z2p22lTiuxbR-ZwEWz-41v/view?usp=sharing


<h2> Splitwise – Group Expense Sharing System (Django)</h2> 

A backend-focused Splitwise-style application built with Django that allows users to create groups, add members, split expenses using multiple strategies, track balances, and compute simplified settlements — all with clean architecture and scalable design.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Features

- 🔐 **User Authentication**
  - Signup, login, logout using Django authentication
  - Only authenticated users can create groups or add expenses

- 👥 **Group Management**
  - Create groups and add multiple members
  - Only group members can view or add expenses

- 💰 **Expense Management**
  - Add expenses with a description, amount, payer, and participants
  - Supports multiple split types:
    - **Equal split**
    - **Exact split**
    - **Percentage split**

- ⚖️ **Balance Tracking**
  - Computes net balance for each user in a group
  - Positive balance → user should receive money
  - Negative balance → user owes money

- 🔁 **Debt Simplification**
  - Calculates the minimum set of transactions required to settle all debts in a group
  - Implements Splitwise-style settlement logic

- 🧾 **Ledger-Based Design**
  - Expenses and settlements are stored as immutable records
  - Balances are always derived from data (no direct balance mutation)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🧠 Architecture & Design Decisions

- **Service Layer Architecture**
  - Business logic separated into services (`GroupService`, `ExpenseService`, `BalanceService`)
  - Views remain thin and focused on request/response handling

- **Strategy Pattern for Expense Splitting**
  - Pluggable split strategies:
    - `EqualSplitStrategy`
    - `ExactSplitStrategy`
    - `PercentageSplitStrategy`
  - Easy to extend with new split types

- **Transactional Integrity**
  - All expense creation operations are wrapped in database transactions
  - Ensures consistency even if errors occur mid-operation

- **Performance Optimizations**
  - Uses `bulk_create` for inserting split records efficiently
  - Avoids unnecessary queries during balance computation

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (development)
- **Auth:** Django Authentication System
- **ORM:** Django ORM
- **Design Patterns:** Strategy Pattern, Service Layer Pattern

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


