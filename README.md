1. Playto Payout Engine

2. Overview

This project is a simplified payout engine where merchants can view balance, request payouts, and track payout status.



3. Tech Stack
* Backend: Django, Django REST Framework
* Database: SQLite (can be switched to PostgreSQL)



4. Setup Instructions

a. Clone the repository
b. Create virtual environment
c. Install dependencies


pip install django djangorestframework psycopg2-binary


d. Run migrations
python manage.py migrate


e.. Run server
python manage.py runserver




5. Features Implemented

* Ledger-based balance system
* Payout creation
* Idempotency handling
* Concurrency-safe transactions
* Payout processing simulation



6. How to Test
Open Django shell:
python manage.py shell

Run:
from payouts.views import create_payout, process_payout
from payouts.models import Merchant

m = Merchant.objects.first()

res = create_payout(m.id, 3000, "test123")
print(res)

print(process_payout(res["payout_id"]))


6. Notes

* All amounts are stored in paise (integer)
* Balance is computed from ledger (not stored directly)
* System handles duplicate requests safely


8. Author

Adarsha Gupta
adarshagupta098@gmail.com
8115708572
