1. Playto Payout Engine – EXPLAINER

Author: Adarsha Gupta
Email:- adarshagupta098@gmail.com
Phone:- +91-8115708572




2. Approach

I focused on building a correct and reliable system rather than just adding features. I tried to think about how real payment systems handle money, especially in cases of multiple requests and failures.



3. a. The Ledger

I did not store balance directly. Instead, I used a ledger system where every transaction is stored as credit or debit.

Balance is calculated using a database query:



This helps avoid errors and ensures the balance is always correct.



4. b. The Lock

To prevent multiple requests from using the same balance, I used:

select_for_update()


This locks the merchant row so only one transaction can run at a time.


5. c. The Idempotency

To handle duplicate requests, I used an idempotency key.

If the same request comes again:

* The system returns the same response
* No new payout is created

This avoids duplicate payouts.


6. d. The State Machine

Payout moves through these states:

* pending → processing → completed
* pending → processing → failed

Invalid transitions are blocked to keep the system consistent.


7. e. The AI Audit

Initially, I thought of calculating balance using Python loops, but realized it is not safe for concurrent requests.

So I switched to database aggregation, which is faster and more reliable.


8. Challenges Faced

Understanding concurrency and idempotency was challenging at first. I learned how to use database locking and transactions to solve these problems.



9. What I am most proud of

* Implemented a ledger-based system
* Handled concurrency safely
* Built idempotent payout logic
* Simulated real payout processing

This helped me understand how real backend systems work.
