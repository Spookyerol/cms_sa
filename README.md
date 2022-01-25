Mini CRM_SA System

Small Django python webapp
Launch by navigating to root directory with manage.py and type "python manage.py runserver" in the console.
"python manage.py shell" will start a command line shell to interact with the DB (or use an sqlite DB browsing tool like SQLiteStudio)

Available paths/actions in CRM/urls.py: (localhost port 8000)

CRM/ - see view "index" in views.py

CRM/users - see view "detail" in CRM/views.py
CRM/users/username - see view "detail" in CRM/views.py

CRM/customer/username/post/ - see view "post_customer" in CRM/views.py
CRM/customer/customer_id/put/ - see view "put_customer" in CRM/views.py
CRM/customer/customer_id/get/ - see view "get_customer" in CRM/views.py

CRM/client/post/ - see view "post_client" in CRM/views.py
CRM/client/client_id/get/ - see view "get_client" in CRM/views.py

CRM/invoice/post/ - see view "post_invoice" in CRM/views.py
CRM/invoice/invoice_no/get/ - see view "get_invoice" in CRM/views.py

Admin page at CRM/admin

Superuser Account:
username = SuperAdmin
password = Password