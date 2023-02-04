import datetime

import pytz
from django.db import models
#from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, get_fixed_timezone
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    is_temp = models.BooleanField('is temporary - flag', 
                                  help_text='Designates whether user is temporary or regular.')
    objects = CustomUserManager()
    def __str__(self):
        return self.username

class CatalogueFoodType(models.Model):
    name = models.CharField('food type name', max_length=30)
    visible = models.BooleanField('food type visibility', default=False)
    
    class Meta:
        verbose_name = 'food type'
        verbose_name_plural = 'food types'
    def __str__(self):
        return self.name

def locality_logo_directory_path(instance, filename):
    return 'logos/{0}/{1}'.format(instance.name, filename)

class Locality(models.Model):
    #loc_id = models.AutoField('locality id', primary_key=True)
    name = models.CharField('locality name', max_length=60)
    food_type = models.ManyToManyField(CatalogueFoodType, through='FoodTypeJunction', related_name='localities')
    logo = models.ImageField('locality logo', upload_to=locality_logo_directory_path)
    #loc_status = models.CharField('locality status', max_length=3, null=False)
    #loc_reg_dt = models.DateField('locality registration date', auto_now_add=True, null=False)
    
    class Meta:
        verbose_name_plural = 'localities'
    def __str__(self):
        return self.name

class FoodTypeJunction(models.Model):
    locality = models.ForeignKey(Locality, models.PROTECT, related_name='food_type_junctions')
    food_type = models.ForeignKey(CatalogueFoodType, models.PROTECT, related_name='food_type_junctions')
        
    class Meta:
        verbose_name_plural = 'food type junctions'
    def __str__(self):
        return "%s - %s" % (self.locality.name, self.food_type.name)
    
class LocalityStatus(models.Model):
    STATUS_CODES = (
            ('ACT', 'Active'),
            ('SUS', 'Suspended'),
            ('END', 'Terminated')
        )
    #loc_stt_id = models.AutoField('locality status id', primary_key=True)
    start_dtm = models.DateTimeField('locality status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('locality status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    code = models.CharField('locality status code', max_length=3, choices=STATUS_CODES)
    remarks = models.CharField('locality status remarks', max_length=100, blank=True)
    locality = models.ForeignKey(Locality, models.CASCADE, related_name='locality_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='locality_statuses')
    
    class Meta:
        verbose_name_plural = 'locality statuses'
    def __str__(self):
        return '%s - Status' % (self.locality.name)
        
class CataloguePoliticalDivision(models.Model):
    corr_id = models.PositiveSmallIntegerField('corregimiento id', primary_key=True)
    corr_name = models.CharField('corregimiento name', max_length=40)
    dist_id = models.PositiveSmallIntegerField('distrito id')
    dist_name = models.CharField('district name', max_length=30)
    prov_id = models.PositiveSmallIntegerField('provincia id')
    prov_name = models.CharField('province name', max_length=30)
    cnty_id = models.PositiveSmallIntegerField('country id')
    cnty_name = models.CharField('country name', max_length=30)

    class Meta:
        verbose_name = 'political division'
        verbose_name_plural = 'political divisions'
    def __str__(self):
        return '%s, %s, %s, %s' % (self.corr_name, self.dist_name, self.prov_name, self.cnty_name)

class Branch(models.Model):
    #brn_id = models.AutoField('branch id', primary_key=True)
    name = models.CharField('branch name', max_length=60)
    address = models.CharField('branch address', max_length=70)
    #brn_status = models.CharField('branch status', max_length=3, null=False)
    #brn_reg_dt = models.DateField('branch registration date', auto_now_add=True, null=False)
    corr = models.ForeignKey(CataloguePoliticalDivision, on_delete=models.PROTECT, related_name='branches')
    locality = models.ForeignKey(Locality, models.CASCADE, related_name='branches')
    user = models.ManyToManyField(User, through='UserAccess', related_name='branches')
    
    class Meta:
        verbose_name_plural = 'branches'
    def __str__(self):
        return '%s - %s' % (self.locality.name, self.name)
    
class BranchStatus(models.Model):
    STATUS_CODES = (
            ('ACT', 'Active'),
            ('SUS', 'Suspended'),
            ('END', 'Terminated')
        )
    start_dtm = models.DateTimeField('branch status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('branch status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    code = models.CharField('branch status code', max_length=3, choices=STATUS_CODES)
    remarks = models.CharField('branch status remarks', max_length=100, blank=True)
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='branch_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='branch_statuses')
    
    class Meta:
        verbose_name_plural = 'branch statuses'
    def __str__(self):
        return '%s - %s - Status' % (self.branch.locality.name, self.branch.name)


class BranchSchedule(models.Model):
    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
        )
    week_day = models.PositiveSmallIntegerField('branch schedule week day', choices=DAYS)
    opening = models.BooleanField('branch schedule - opening flag', default=True)
    open_tm = models.TimeField('branch schedule opening time')
    close_tm = models.TimeField('branch schedule closing time')
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='branch_schedules')
    
    class Meta:
        verbose_name_plural = 'branch schedules'
    def __str__(self):
        return '%s - %s - Schedule - DOW %s' % (self.branch.locality.name, self.branch.name, self.week_day)
    
class UserAccess(models.Model):
    branch = models.ForeignKey(Branch, models.PROTECT, related_name='user_accesses')
    user = models.ForeignKey(User, models.PROTECT, related_name='user_accesses')
        
    class Meta:
        verbose_name_plural = 'user accesses'
    def __str__(self):
        return "User %s - Branch %s" % (self.user.username, self.branch.id)
    
def qrcode_directory_path(instance, filename):
    return 'qrcodes/{0}/{1}/{2}'.format(instance.branch.locality.id, instance.branch.id, filename)
    
class QRCode(models.Model): #How do we limit the amount of QRCodes that a branch can have?
    #qrc_id = models.AutoField('qr code id', primary_key=True)
    table_num = models.PositiveSmallIntegerField('qr code table number')
    name = models.CharField('qr code name', max_length=50)
    qrcode = models.ImageField('qr code image', upload_to=qrcode_directory_path)
    url = models.URLField('qr code url', max_length=200)
    #qrc_status = models.CharField('qr code status', max_length=3, null=False)    
    #qrc_reg_dt = models.DateField('qr code registration date', auto_now_add=True, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='qr_codes')
    
    class Meta:
        verbose_name = 'qr code'
        verbose_name_plural = 'qr codes'
    def __str__(self):
        return '%s - %s - Table %s QR' % (self.branch.locality.name, self.branch.name, self.table_num)
    
class QRCodeStatus(models.Model):
    STATUS_CODES = (
            ('ACT', 'Active'),
            ('INA', 'Inactive'),
            ('DEL', 'Deleted') 
        )
    start_dtm = models.DateTimeField('qr code status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('qr code status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    #name = models.CharField('qr code name', max_length=50)
    code = models.CharField('qr code status code', max_length=3, choices=STATUS_CODES)
    remarks = models.CharField('qr code status remarks', max_length=100, blank=True)
    qrcode = models.ForeignKey(QRCode, models.CASCADE, related_name='qr_codes_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='qr_codes_statuses')
    
    class Meta:
        verbose_name_plural = 'qr codes statuses'
    def __str__(self):
        return '%s - %s - Table %s QR - Status' % (self.qrcode.branch.locality.name,
                                       self.qrcode.branch.name, self.qrcode.table_num)
    
class Order(models.Model):
    #ord_id = models.AutoField('order id', primary_key=True)
    #name = models.CharField('order client name', max_length=20)
    notes = models.CharField('order notes', max_length=250)
    #ord_qty = models.SmallIntegerField('order quantity', null=False, default=1)
    #ord_status = models.CharField('order status', max_length=3, null=False)
    #itm_fk = models.ForeignKey(Items, on_delete=models.SET_NULL, db_column='itm_id', null=True)
    qrcode = models.ForeignKey(QRCode, models.CASCADE, related_name='orders')

    def __str__(self):
        return '%s - %s - Order for %s' % (self.qrcode.branch.locality.name,
                                       self.qrcode.branch.name, self.name)
    #def status(self):
        #pass
    #Must add custom methods (def questions to ask the terminal) for all types of order status, as well as a timer.
    
class OrderStatus(models.Model):
    STATUS_CODES = (
            ('NEW', 'Order received'),
            ('CON', 'Order confirmed'),
            ('ADD', 'Item(s) added'),
            ('REM', 'Item(s) removed'),
            ('DSC', 'Discount added'),
            ('CPL', 'Order completed'),
            #('UNP', 'Order left unpaid'), #Remove this?
            ('CXL', 'Order cancelled by staff'),
            ('SYS', 'Order cancelled automatically by system (order timeout)')
        )
    start_dtm = models.DateTimeField('order status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('order status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    code = models.CharField('order status code', max_length=3, choices=STATUS_CODES)
    discount = models.DecimalField('order discount', max_digits=3, decimal_places=2, default=0.00)
    remarks = models.CharField('order status remarks', max_length=100, blank=True)
    order = models.ForeignKey(Order, models.CASCADE, related_name='order_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='order_statuses')
    
    class Meta:
        verbose_name_plural = 'order statuses'
    def __str__(self):
        return '%s - %s - Order for %s - Status' % (self.order.qrcode.branch.locality.name,
                                       self.order.qrcode.branch.name, self.order.name)
    
def category_image_directory_path(instance, filename):
    return 'categories/{0}/{1}'.format(instance.locality.id, filename)

class Category(models.Model):
    name = models.CharField('category name', max_length=50)
    description = models.CharField('category description', max_length=100, blank=True)
    image_path = models.ImageField('category image path', upload_to=category_image_directory_path, blank=True)
    sequence = models.PositiveSmallIntegerField('category sequence number')
    locality = models.ForeignKey(Locality, models.CASCADE, related_name='categories')
    
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return '%s - %s' % (self.locality.name, self.name)

    def current_status_cat(self):
        return CategoryStatus.objects.filter(category = self, end_dtm = datetime.datetime(2038, 1, 1, 0, 0, tzinfo=pytz.utc))
    
class CategoryStatus(models.Model):
    STATUS_CODES = (
            ('ACT', 'Active'),
            ('INA', 'Inactive'),
            ('DEL', 'Deleted')
        )
    start_dtm = models.DateTimeField('category status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('category status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    code = models.CharField('category status code', max_length=3, choices=STATUS_CODES)
    remarks = models.CharField('category status remarks', max_length=100, blank=True)
    category = models.ForeignKey(Category, models.CASCADE, related_name='category_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='category_statuses')
    
    class Meta:
        verbose_name_plural = 'category statuses'
    def __str__(self):
        return '%s - %s - Status' % (self.category.locality.name, self.category.name)
    
def item_image_directory_path(instance, filename):
    return 'items/{0}/{1}/{2}'.format(instance.category.locality.id, instance.category.id, filename)

class Item(models.Model):
    TAXES = (
            (0.00, 'Exento - 0%'),
            (0.07, 'Regular - 7%'),
            (0.10, 'Licor - 10%'),
            (0.15, 'Tabaco - 15%')
        )
    #itm_id = models.AutoField('item id', primary_key=True)
    name = models.CharField('item name', max_length=50)
    description = models.CharField('item description', max_length=100, blank=True)
    tax_rate = models.DecimalField('item tax rate', max_digits=3, decimal_places=2, default=0.07, choices=TAXES)
    #itm_price = models.DecimalField('item price', max_digits=5, decimal_places=2)
    image_path = models.ImageField('item image path', upload_to=item_image_directory_path, blank=True)
    #itm_avail = models.BooleanField('item availability', default=True, null=False)
    #itm_status = models.CharField('item status', max_length=3, null=False)
    sequence = models.PositiveSmallIntegerField('item sequence number')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    branch = models.ManyToManyField(Branch, through='ItemStatus', related_name='items')
    junction = models.ManyToManyField(OrderStatus, through='OrderJunction', related_name='items')

    def current_status(self):
        return ItemStatus.objects.filter(item = self, end_dtm = datetime.datetime(2038, 1, 1, 0, 0, tzinfo=pytz.utc))
    
    def __str__(self):
        return '%s - %s' % (self.category.locality.name, self.name)
    
class ItemStatus(models.Model):
    STATUS_CODES = (
            ('ACT', 'Active'),
            ('DSC', 'Discounted'),
            ('DSX', 'Discontinued')
        )
    AVAILABILITY = (
        ('AVL', 'Available'),
        ('OOS', 'Out of Stock'),
        ('OSH', 'Out of Stock - Hidden')
        )
    start_dtm = models.DateTimeField('item status beginning datetime', auto_now_add=True)
    end_dtm = models.DateTimeField('item status end datetime', 
                                   default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
    code = models.CharField('item status code', max_length=3, choices=STATUS_CODES)
    price = models.DecimalField('item price', max_digits=5, decimal_places=2)
    discount = models.DecimalField('item discount', max_digits=3, decimal_places=2, default=0.00)
    #availability = models.BooleanField('item availability', default=True)
    availability = models.CharField('item availability', max_length=3, choices=AVAILABILITY)
    remarks = models.CharField('item status remarks', max_length=100, blank=True)
    item = models.ForeignKey(Item, models.CASCADE, related_name='item_statuses')
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='item_statuses')
    user = models.ForeignKey(User, models.RESTRICT, related_name='item_statuses')
    
    class Meta:
        verbose_name_plural = 'item statuses'
    def __str__(self):
        return '%s - %s - Status (Branch %s)' % (self.item.category.locality.name, self.item.name, self.branch.id)

    
class ItemOption(models.Model):
    description = models.CharField('item option description', max_length=100)
    #price = models.DecimalField('item option price', max_digits=5, decimal_places=2, default=0.00)
    min_selections = models.PositiveSmallIntegerField('item option min selections', default=0)
    max_selections = models.PositiveSmallIntegerField('item option max selections')
    optional = models.BooleanField('item option - optional flag', default=False)
    sequence = models.PositiveSmallIntegerField('item option sequence number')
    item = models.ForeignKey(Item, models.CASCADE, related_name='item_options')
    
    class Meta:
        verbose_name_plural = 'item options'
    def __str__(self):
        return '%s - %s' % (self.item.name, self.description)
    
class ItemOptionResponse(models.Model):
    description = models.CharField('item option response description', max_length=100)
    price = models.DecimalField('item option response price', max_digits=5, decimal_places=2, default=0.00)
    max_quantity = models.PositiveSmallIntegerField('item option response max quantity', default=1)
    sequence = models.PositiveSmallIntegerField('item option response sequence number')
    item_option = models.ForeignKey(ItemOption, models.CASCADE, related_name='item_option_responses')
    
    class Meta:
        verbose_name_plural = 'item option responses'
    def __str__(self):
        return '%s - %s - %s' % (self.item_option.item.name, self.item_option.description, self.description)
    
class OrderJunction(models.Model):
    #start_dtm = models.DateTimeField('order junction beginning datetime', auto_now_add=True)
    order_status = models.ForeignKey(OrderStatus, models.CASCADE, related_name='order_junctions')
    item = models.ForeignKey(Item, models.CASCADE, related_name='order_junctions')
    quantity = models.SmallIntegerField('order junction quantity', default=1)
    discount = models.DecimalField('item discount in-order', max_digits=3, decimal_places=2, default=0.00)
    remarks = models.CharField('order junction notes', max_length=250, blank=True)
    options = models.ManyToManyField(ItemOptionResponse, through='OrderJunctionOption', related_name='order_juntions')
    
    class Meta:
        verbose_name_plural = 'order junctions'
    def __str__(self):
        return 'Order %s - %s' % (self.order.id, self.item.name)
    
class OrderJunctionOption(models.Model):
    order_junction = models.ForeignKey(OrderJunction, models.CASCADE, related_name='order_junction_options')
    item_option_response = models.ForeignKey(ItemOptionResponse, models.CASCADE, related_name='order_junction_options')
    quantity = models.PositiveSmallIntegerField('order junction option quantity', default=1)
    
    class Meta:
        verbose_name_plural = 'order junction options'
    def __str__(self):
        return 'Order %s - %s Option' % (self.order.id, self.item.name)