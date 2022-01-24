from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import User, Invoice, Customer, Client

from datetime import datetime, timezone


# Create your views here.
def index(request):
    user_list = User.objects.all()
    customer_list = Customer.objects.all()
    return render(request, 'CRM/index.html', {'user_list': user_list, 'customer_list' : customer_list})

def detail(request, username=None):
    recent3_invoices = Invoice.objects.order_by('-invoice_date')[:3]
    output = ""
    for i in recent3_invoices: #form string
        
        if not i.paid:
            output += "not paid "
        else:
            output += "paid "
            
        if i.user: #invoice linked to user
            output += "%d %s %s" % (i.amount, i.user.currency, i.user.username)
        else: #external invoice
            output += "%d %s %s" % (i.amount, i.currency, i.invoice_external_id)
        output += '<br>'
    
    output += '<br><br>'
    if username: #list items for a specific user in the url
        user = User.objects.get(pk=username)
        user_invoices = user.invoice_set.all()
        
        now = datetime.now(timezone.utc)
        limit = datetime(now.year-1, now.month, now.day, now.hour, now.minute, now.second, now.microsecond, now.tzinfo)
        
        total = 0 #calculate total amount invoiced to this user
        for i in user_invoices:
            output += str(i)
            output += '<br>'
            
            if i.invoice_date >= limit:
                total += i.amount
         
        output += '<br>'
        output += "Total invoiced amount to %s is %d %ss." % (username, total, user.currency)
        
        output += '<br><br>'
        output += "Unpaid Invoices for user %s:<br>" % (username)
        
        for i in user_invoices:
            if not i.paid:
                output += str(i)
                output += '<br>'
    
    return HttpResponse(output)

def post_customer(request, username):
    user = get_object_or_404(User, pk=username) #get the user that the customer will be associated with
    if request.method == 'POST':
        try: #get POST data from form fields
            cs_first_name = request.POST.get('cs_first_name')
            cs_last_name = request.POST.get('cs_last_name')
            cs_email = request.POST.get('cs_email')
            cs_country = request.POST.get('cs_country')
            cs_company = request.POST.get('cs_company')
        except (KeyError):
            return render(request, 'CRM/post_customer.html', {
                'user' : user,
                'error_message' : "Fill in required fields.",
            })
        else:
            user.customer = Customer(cs_first_name = cs_first_name, #create Customer instance for the user
                                     cs_last_name = cs_last_name,
                                     cs_email = cs_email,
                                     cs_country = cs_country,
                                     cs_company = cs_company)
            user.customer.save()
            customer_id = user.customer.id
            return render(request, 'CRM/post_customer.html', {'user' : user, 'customer_id' : customer_id})
    else: #if just loading the html page
        try:
            customer_id = user.customer.id
        except (KeyError, Customer.DoesNotExist):
            return render(request, 'CRM/post_customer.html', {'user' : user}) #just render the page
        else:
            return render(request, 'CRM/post_customer.html', {'user' : user, 'customer_id' : customer_id}) #if user already has a customer a warning will be displayed

def put_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    
    if request.method == 'POST':
        try: #get POST data from form fields - html forms do not support a PUT method type
            cs_first_name = request.POST.get('cs_first_name')
            cs_last_name = request.POST.get('cs_last_name')
            cs_email = request.POST.get('cs_email')
            cs_country = request.POST.get('cs_country')
            cs_company = request.POST.get('cs_company')
            
            if request.POST.get('cs_open_payment') == 'on': #map checkmark values to bools
                cs_open_payment = True
            else:
                cs_open_payment = False
                
        except (KeyError):
            return render(request, 'CRM/put_customer.html', {
                'customer' : customer,
                'error_message' : "Fill in required fields.",
            })
        else: #update the customers information with new data
            customer.cs_first_name = cs_first_name
            customer.cs_last_name = cs_last_name
            customer.cs_email = cs_email
            customer.cs_country = cs_country
            customer.cs_company = cs_company
            customer.cs_open_payment = cs_open_payment
    
            customer.save()
            
            return render(request, 'CRM/put_customer.html', {'customer' : customer})
    else: #if just loading the html page
        return render(request, 'CRM/put_customer.html', {'customer' : customer})
    
def get_customer(request, customer_id): #typing http://localhost:8000/CRM/customer/customer_id/get/ will call this view
    customer = get_object_or_404(Customer, pk=customer_id)
    
    output = customer.cs_first_name
    output += " " + customer.cs_last_name + "<br>"
    output += customer.cs_email + "<br>"
    if customer.cs_open_payment == False:
        output += "Open payments" + "<br><br>"
    else:
        output += "No open payments" + "<br><br>"
    output += "ID = " + str(customer.id)
    
    return HttpResponse(output) #output is a string construction of the customer instance
        
def post_client(request):
    
    if request.method == 'POST':
        try: #get POST data from form fields
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            company = request.POST.get('company')
            cl_external_id = request.POST.get('cl_external_id')
        except(KeyError):
            return render(request, 'CRM/post_client.html', {
                'error_message' : "Fill in required fields.",
                })
        else:
            client = None
            for c in Client.objects.all(): #check that the client does not already exist
                if(c.cl_external_id == cl_external_id):
                    client = c
                    break
                
            if not client: #client does not exist - create new instance
                client = Client(firstname = firstname,
                                lastname = lastname,
                                email = email,
                                company = company,
                                cl_external_id = cl_external_id)
                
                client.save()
                return render(request, 'CRM/post_client.html', {'client' : client})
            
            else: #cient does exist - update existing client (you could also raise an error/warning instead)
                client.firstname = firstname
                client.lastname = lastname
                client.email = email
                client.company = company
                client.cl_external_id = cl_external_id
                
                client.save()
                return render(request, 'CRM/post_client.html', {'client' : client})
    else:
        return render(request, 'CRM/post_client.html')
    
def get_client(request, client_id): #typing http://localhost:8000/CRM/client/client_id/get/ will call this view
    client = get_object_or_404(Client, pk=client_id)
    
    output = client.firstname
    output += " " + client.lastname + "<br>"
    output += client.email + "<br>"
    output += client.cl_external_id + "<br>"
    output += "ID = " + str(client.id)
    
    return HttpResponse(output) #output is a string construction of the client instance
    
def post_invoice(request):
    
    if request.method == 'POST': #get POST data from form fields
        invoice_external_id = request.POST.get('invoice_external_id')
        cl_external_id = request.POST.get('cl_external_id')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        
        client_exists = False #invoices generated through this POST will not have users on creation and instead have external IDs
        for c in Client.objects.all():
            if c.cl_external_id == cl_external_id:
                client_exists = True
                break
        
        if not client_exists: #make sure that there is a client to link, otherwise we just have an invoice with no tangible owner in the database
            return render(request, 'CRM/post_invoice.html', {
                'error_message' : "The specified client ID does not exist.",
                })
        else:
            amount = '{:.2f}'.format(float(amount))
            
            invoice = None
            error_message = None
            for i in Invoice.objects.all(): #checks if this invoice already exists
                if i.invoice_external_id == invoice_external_id:
                    invoice = i
                    error_message = "An invoice with this ID already exists and has been edited"
                    break
                
            if not invoice: #no invoice exists so we create a new instance
                invoice = Invoice(invoice_external_id = invoice_external_id,
                                  cl_external_id = cl_external_id,
                                  amount = amount,
                                  currency = currency,
                                  invoice_date = datetime.now(timezone.utc))
            else: #an invoice exists so instead we edit the pre-existing one - might choose to error out here instead however
                invoice.cl_external_id = cl_external_id
                invoice.amount = amount
                invoice.currency = currency
                invoice.invoice_date = datetime.now(timezone.utc) #since the invoice is updated the date is set to the date of the most recent update
                
            invoice.save()
            
            return render(request, 'CRM/post_invoice.html', {'invoice_no' : invoice.invoice_no,
                                                             'paid' : invoice.paid,
                                                             'error_message' : error_message
                                                            }) #paid == False is analogous to open_invoice == True
    else:
        return render(request, 'CRM/post_invoice.html')
    
def get_invoice(request, invoice_no): #typing http://localhost:8000/CRM/invoice/OTA-XXXXX/get/ will call this view
    invoice = get_object_or_404(Invoice, pk=invoice_no)
    
    output = ""
    
    if invoice.invoice_external_id: #this field might be null
        output += invoice.invoice_external_id + "<br>"
    else:
        output += "None" + "<br>"
    
    if invoice.cl_external_id: #this field might be null
        output += invoice.cl_external_id + "<br>"
    else:
        output += "None" + "<br>"
        
    output += "Is paid: " + str(invoice.paid) + "<br>" #paid == False is analogous to open_invoice == True
    output += str(invoice.amount) + "<br>"
    
    if invoice.currency: #if the invoice has it's own currency prefer to post that
        output += invoice.currency
    else: #if the invoice doesn't have a currency, then it hasn't been generated by open_invoice and so has a user with currency
        output += "User currency: " + invoice.user.currency + "<br>"
    
    return HttpResponse(output)











    
    
    