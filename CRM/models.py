from django.db import models

from datetime import datetime, timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, unique=True, null=False, max_length=32)
    email = models.EmailField(max_length=256)
    company_name = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    currency = models.CharField(max_length=32)
    invoicedOver1000 = models.BooleanField(default=False, editable=False)
    
    def __str__(self):
        return self.username + " " + self.email
    
    def get_invoices(self):
        return self.invoice_set.objects.all()
    
    def invoiced_over_1000(self):
        invoices = self.invoice_set.objects.all()
        
        for i in invoices:
            if i.amount > 1000:
                self.invoicedOver1000 = True
                return self.invoicedOver1000
        self.invoicedOver1000 = False
        return self.invoicedOver1000
    
    def total_invoiced_last_12_months(self):
        user_invoices = self.invoice_set.all()
        
        now = datetime.now(timezone.utc)
        limit = datetime(now.year-1, now.month, now.day, now.hour, now.minute, now.second, now.microsecond, now.tzinfo)
        
        total = 0
        
        for i in user_invoices:
            
            if i.invoice_date >= limit:
                total += i.amount
                
        return total

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    invoice_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    
    invoice_no = models.CharField(primary_key=True, max_length=9, null=False, default=-1, unique=True)
    
    invoice_external_id = models.CharField(max_length=256, unique=True, null=True)
    cl_external_id = models.CharField(max_length=256, null=True)
    currency = models.CharField(max_length=32, null=True)
    
    def save(self, *args, **kwargs): #overload save for custom behaviour
        if self.invoice_no == -1: #the default of -1 is a dummy value - we now auto-generate the proper ID in format OTA-XXXXX in order where XXXXX is a number
            prefix = "OTA-" 
            prev_instances = self.__class__.objects
            
            if prev_instances.exists(): #check the XXXXX portion of the previous invoices ID and increment by 1
                last_instance_id = prev_instances.last().invoice_no[-5:]
                self.invoice_no = prefix + '{0:05d}'.format(int(last_instance_id)+1)
            else:
                self.invoice_no = prefix + '{0:05d}'.format(1)
                
        if float(self.amount) > 1000: #if invoice.amount is over 1000 make sure the associated user has the correct flag
            self.user.invoicedOver1000 = True
                
        super(Invoice, self).save(*args, **kwargs)
        
    def __str__(self):
        if self.user:
            return str(self.user.username) + " " + str(self.amount) + " " + str(self.user.currency) + "s"
        else: #post_invoices in views.py will generate invoices without users
            return str(self.invoice_external_id) + " " + str(self.amount) + " " + str(self.currency) + "s"
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    cs_first_name = models.CharField(max_length=64, null=False)
    cs_last_name = models.CharField(max_length=64, null=False)
    cs_email = models.EmailField(max_length=256, null=False)
    cs_country = models.CharField(max_length=256)
    cs_company = models.CharField(max_length=256)
    cs_open_payment = models.BooleanField(default=False) #has to be manually corrected on initial creation
    
    def save(self, *args, **kwargs): #overload save to fix cs_open_payment
        if self.cs_open_payment == False:
            self.cs_open_payment = self.has_unpaid_invoices(self)
        
        super(Invoice, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.cs_first_name) + " " + str(self.cs_last_name)
    
    def has_unpaid_invoices(self): #supposed help set cs_open_payment but not tested
        invoices = self.user.invoice_set.all()
        
        for i in invoices:
            if not i.paid:
                return True
        return False

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    firstname = models.CharField(max_length=64, null=False)
    lastname = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=256)
    company = models.CharField(max_length=256)
    cl_external_id = models.CharField(max_length=256, null=False, unique=True)
    
    def __str__(self):
        return str(self.firstname) + " " + str(self.lastname)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    