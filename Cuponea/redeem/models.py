import uuid #, datetime,
#import pytz
from django.db import models
from django.contrib.auth import get_user_model
#from django.utils.dateparse import parse_datetime
from django.utils.timezone import now # make_aware, get_fixed_timezone
#from django.apps import apps
#from panel.apps import PanelConfig

class CatalogueFoodType(models.Model):
    name = models.CharField('food type name', max_length=30)
    visible = models.BooleanField('food type visibility', default=False)
    
    class Meta:
        verbose_name = 'food type'
        verbose_name_plural = 'food types'
    def __str__(self):
        return self.name
    #Must create some test later to ensure no restaurant is registered on more than N food types.

# def locality_logo_directory_path(instance, filename): #TEMP, DELETE
    # return 'logos/{0}/{1}'.format(instance.name, filename)

def business_logo_directory_path(instance, filename):
    return 'logos/{0}/{1}'.format(instance.name, filename)

class Business(models.Model):
    STATUS = (
        ('ACT', 'Business active'),
        ('INA', 'Business inactive')
        )
    name = models.CharField('business name', max_length=60, unique=True)
    food_type = models.ManyToManyField(CatalogueFoodType, through='FoodTypeJunction')
    logo = models.ImageField('business logo', upload_to=business_logo_directory_path)
    time_available = models.IntegerField('business time available', default=0)
    time_exp_date = models.DateField('business time expiration date')
    status = models.CharField('business status', max_length=3, choices=STATUS)
    
    # Uncomment this when second app exists and this can point to latest status.
    # def current_status(self):
    #     return BusinessStatus.objects.filter(business = self, end_dtm = datetime.datetime(2038, 1, 1, 0, 0, tzinfo=pytz.utc))
    
    class Meta:
        verbose_name_plural = 'businesses'
    def __str__(self):
        return self.name

class FoodTypeJunction(models.Model):
    business = models.ForeignKey(Business, models.PROTECT, related_name='food_type_junctions')
    food_type = models.ForeignKey(CatalogueFoodType, models.PROTECT, related_name='food_type_junctions')
        
    class Meta:
        verbose_name_plural = 'food type junctions'
        unique_together = (('business', 'food_type'),)
    def __str__(self):
        return "%s - %s" % (self.business.name, self.food_type.name)
   
# Status tables based on history of changes will come in next app.
# class BusinessStatus(models.Model):
#     STATUS_CODES = (
#             ('ACT', 'Active'),
#             ('SUS', 'Suspended'),
#             ('END', 'Terminated')
#         )
#     start_dtm = models.DateTimeField('business status start datetime', auto_now_add=True)
#     end_dtm = models.DateTimeField('business status end datetime', 
#                                    default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
#     code = models.CharField('business status code', max_length=3, choices=STATUS_CODES)
#     remarks = models.CharField('business status remarks', max_length=100, blank=True)
#     business = models.ForeignKey(Business, models.CASCADE, related_name='business_statuses')
#     #user = models.ForeignKey(User, models.RESTRICT, related_name='business_statuses')
    
#     class Meta:
#         verbose_name_plural = 'business statuses'
#     def __str__(self):
#         return '%s - Status' % (self.business.name)
        
class CataloguePoliticalDivision(models.Model):
    corr_name = models.CharField('corregimiento name', max_length=40)
    #dist_name = models.CharField('district name', max_length=30)
    #prov_name = models.CharField('province name', max_length=30)
    #cnty_name = models.CharField('country name', max_length=30)

    class Meta:
        verbose_name = 'political division'
        verbose_name_plural = 'political divisions'
    def __str__(self):
        return '%s' % (self.corr_name) #, self.dist_name, self.prov_name, self.cnty_name)

class Branch(models.Model):
    STATUS = (
        ('ACT', 'Branch active'),
        ('INA', 'Branch inactive')
        )
    name = models.CharField('branch name', max_length=60)
    address = models.CharField('branch address', max_length=70)
    website = models.URLField('branch website URL', max_length=200, blank=True)
    phone = models.CharField('branch phone number', max_length=8, blank=True) #Best way to validate this? Via test?
    description = models.CharField('branch description', max_length=300)
    latitude = models.FloatField('branch latitude')
    longitude = models.FloatField('branch longitude')
    status = models.CharField('business branch status', max_length=3, choices=STATUS)
        #Also, maybe add test for min length?
        #Finally, best way to store lan/lon? Use Point from additional package or just two floats?
            #For now, using Floats. If need be might convert to Geo DB or create a parallel one.
    corr = models.ForeignKey(CataloguePoliticalDivision, on_delete=models.PROTECT, related_name='branches')
    business = models.ForeignKey(Business, models.CASCADE, related_name='branches')
    staff_info = models.ManyToManyField(get_user_model(), through='panel.StaffInfo') #apps.get_model('panel', 'StaffInfo')) 
    #user = models.ManyToManyField(User, through='UserAccess')
    
    # Uncomment this when second app exists and this can point to latest status.
    # def current_status(self):
    #     return BranchStatus.objects.filter(branch = self, end_dtm = datetime.datetime(2038, 1, 1, 0, 0, tzinfo=pytz.utc))
    
    class Meta:
        verbose_name_plural = 'branches'
    def __str__(self):
        return '%s %s' % (self.business.name, self.name)

# Status tables based on history of changes will come in next app.
# class BranchStatus(models.Model):
#     STATUS_CODES = (
#             ('ACT', 'Active'),
#             ('SUS', 'Suspended'),
#             ('END', 'Terminated')
#         ) #Add Status Codes for changes in main table, not necessarily status only. Do this for other status tables. This way we can track everything.
#     start_dtm = models.DateTimeField('branch status start datetime', auto_now_add=True)
#     end_dtm = models.DateTimeField('branch status end datetime', 
#                                    default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
#     code = models.CharField('branch status code', max_length=3, choices=STATUS_CODES)
#     remarks = models.CharField('branch status remarks', max_length=100, blank=True)
#     branch = models.ForeignKey(Branch, models.CASCADE, related_name='branch_statuses')
#     #user = models.ForeignKey(User, models.RESTRICT, related_name='branch_statuses')
    
#     class Meta:
#         verbose_name_plural = 'branch statuses'
#     def __str__(self):
#         return '%s - %s - Status' % (self.branch.business.name, self.branch.name)


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
    week_day = models.PositiveSmallIntegerField('branch schedule week day', choices=DAYS, editable=False)
    opening = models.BooleanField('branch schedule - opening flag', default=True)
    open_tm = models.TimeField('branch schedule opening time')
    close_tm = models.TimeField('branch schedule closing time')
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='branch_schedules')
    #Add test to prevent restaurants from placing offers outside open hours.
    
    class Meta:
        verbose_name_plural = 'branch schedules'
    def __str__(self):
        return '%s - %s - DOW %s' % (self.branch.business.name, self.branch.name, self.week_day)
    
# def item_image_directory_path(instance, filename): #TEMP, DELETE
     # return 'items/{0}/{1}'.format(instance.business.id, filename)

# class Item(models.Model):
#     name = models.CharField('item name', max_length=50)
#     description = models.CharField('item description', max_length=100, blank=True)
#     image_path = models.ImageField('item image path', upload_to=item_image_directory_path, blank=True)
#     business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='items')

#     # Uncomment this when second app exists and this can point to latest status.
#     # def current_status(self):
#     #     return ItemStatus.objects.filter(item = self, end_dtm = datetime.datetime(2038, 1, 1, 0, 0, tzinfo=pytz.utc))
    
#     class Meta:
#         verbose_name_plural = 'items'
#     def __str__(self):
#         return '%s - %s' % (self.business.name, self.name)
    
# Status tables based on history of changes will come in next app.
# class ItemStatus(models.Model):
#     STATUS_CODES = (
#             ('ENA', 'Enabled'),
#             ('DIS', 'Disabled'),
#             ('DEL', 'Deleted')
#         )
#     start_dtm = models.DateTimeField('item status start datetime', auto_now_add=True)
#     end_dtm = models.DateTimeField('item status end datetime', 
#                                    default=make_aware(parse_datetime("2038-01-01 00:00:00"), get_fixed_timezone(0)))
#     code = models.CharField('item status code', max_length=3, choices=STATUS_CODES)
#     price = models.DecimalField('item price', max_digits=5, decimal_places=2)
#     remarks = models.CharField('item status remarks', max_length=100, blank=True)
#     item = models.ForeignKey(Item, models.CASCADE, related_name='item_statuses')
#     #user = models.ForeignKey(User, models.RESTRICT, related_name='item_statuses')
    
#     class Meta:
#         verbose_name_plural = 'item statuses'
#     def __str__(self):
#         return '%s - %s - Status' % (self.item.business.name, self.item.name)
    
def offer_image_directory_path(instance, filename):
    return 'offers/{0}/{1}'.format(instance.branch.business.id, filename)

class Offer(models.Model):
    CXL_TYPES = (
        (0, 'Not cancelled'),
        (1, 'Cancelled by staff before start time'),
        (2, 'Cancelled while offer live'),
        (3, 'Cancelled by Cuponea')
        )
    RED_TYPES = (
        (0, 'Regular Offer'),
        (1, 'Flash Offer')
        )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('offer name', max_length=50) #Check lengths with Alex
    description = models.CharField('offer description', max_length=100) #Should we allow blanks here?
    redemption_type = models.PositiveSmallIntegerField('offer redemption type', choices=RED_TYPES)
    image_path = models.ImageField('item image path', upload_to=offer_image_directory_path, blank=True)
    #time = models.PositiveSmallIntegerField('offer time in minutes') #Is small integer okay here?
    start_dtm = models.DateTimeField('offer start datetime')
    end_dtm = models.DateTimeField('offer end datetime')
    original_value = models.DecimalField('offer original value', max_digits=5, decimal_places=2, null=True, blank=True)
    discounted_value = models.DecimalField('offer discounted value', max_digits=5, decimal_places=2, null=True, blank=True)
    cxl_type = models.PositiveSmallIntegerField('offer cancellation type', choices=CXL_TYPES, default=0)
    #amount = models.
    #item = models.ManyToManyField(Item, through='OfferItem')
    branch = models.ManyToManyField(Branch, through='BranchOfferJunction')
    #Is this business foreign key really necessary here?
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='offers')
    #branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='offers')
    #business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='offers')
    
    
    class Meta:
        verbose_name_plural = 'offers'
        indexes = [
            models.Index(fields=['start_dtm'], name='start_dtm_idx'),
            models.Index(fields=['end_dtm'], name='end_dtm_idx'),
            models.Index(fields=['start_dtm', 'end_dtm'], name='active_offers_idx'),
        ]
    def __str__(self):
        return '%s - %s' % (self.business.name, self.name)
    #When creating tests and second app is done, create a test where an Offer
    #can only come if both Business and Branch statuses are Active.
    
# class OfferItem(models.Model):
#     OFFER_TYPES = (
#             ('MUL', 'Multiples'),
#             ('PER', 'Discount in % amount'),
#             ('DOL', 'Discount in $ amount'),
#             ('TOT', 'Total amount for selection')
#         )
#     #Add Test to ensure that amount doesn't pass 5 when using Multiplier, or 1 when Percentage
#     offer_type = models.CharField('offer type code', max_length=3, choices=OFFER_TYPES)
#     amount = models.DecimalField('offer amount', max_digits=5, decimal_places=2)
#     offer = models.ForeignKey(Offer, models.CASCADE, related_name='offer_items')
#     item = models.ForeignKey(Item, models.CASCADE, related_name='offer_items')
    
#     class Meta:
#         verbose_name_plural = 'offer items'
#     def __str__(self):
#         return '%s - Offer #%s - Item #%s' % (self.item.business.name, self.offer.id, self.item.id)
    
#Is an OfferStatus table useful or necessary?
#Add functionality for multiple items per order line (Like 'Pizza AND Shake for 7.50' or 'Burger AND Fries OR Soda' )
#How do we allow for ANDs and ORs within OfferItems?

class BranchOfferJunction(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_offer_junctions')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='branch_offer_junctions')
    
    class Meta:
        verbose_name_plural = 'branch offer junctions'
        unique_together = (('branch', 'offer'),)
    def __str__(self):
        return "%s - %s - %s" % (self.branch.business.name, self.branch.name, self.offer.name)


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Consider making the code field nullable and changing the view.
    # This method might be quicker than doing a while loop through the entire table
    #code = models.CharField('coupon code', max_length=4)
    #start_dtm = models.DateTimeField('coupon start datetime', default=now) #, auto_now_add=True)
    #end_dtm = models.DateTimeField('coupon end datetime')
    use_dtm = models.DateTimeField('coupon use datetime', auto_now=True)
   #redeemed = models.BooleanField('coupon redeemed flag', default=False)
    offer = models.ForeignKey(Offer, models.CASCADE, related_name= 'coupons')
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='coupons')
    user = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='coupons_user')
    #staff = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='coupons_staff')
    
    class Meta:
        verbose_name_plural = 'coupons'
        #Check indexes again when we finish changing the views for new redemption method.
        indexes = [
            #models.Index(fields=['code'], name='code_check_idx' ),
            #models.Index(fields=['code', 'offer_id'], name='code_validating_idx' ),
            models.Index(fields=['user_id', 'offer_id'], name='user_invalid_attempt_idx'),
            #models.Index(fields=['user_id', 'end_dtm'], name='user_history_idx')
        ]
    # def save(self, force_insert=False, using='default'):
    #     if self.end_dtm is None:
    #         self.end_dtm = self.start_dtm + datetime.timedelta(minutes=5)
    #         super(Coupon, self).save(force_insert, using)
    def __str__(self):
        return '%s - Coupon # %s' % (self.offer.business.name, self.id)
        #Verify that this is done properly this way
        #Add test so that end_dtm is never more than start_dtm + timedelta
    
    #Tests to add:
        #Avoid ambiguous characters and exclude from character set (0 vs O)
        #A coupon code can never repeat while another with same name is active
        
# Table to add: One with a history of where the users were physically upon opening the app


class UserLookup(models.Model):
    latitude = models.FloatField('user lookup latitude')
    longitude = models.FloatField('user lookup longitude')
    timestamp = models.DateTimeField('user lookup timestamp', auto_now_add=True)
    redemption = models.BooleanField('user lookup redemption flag', default=False)
    user = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='user_lookups')

    class Meta:
        verbose_name_plural = 'user lookups'
    def __str__(self):
        if self.user != None:
            return '%s - %s' % (self.user.username, self.timestamp)
        else:
            return 'N/A - %s' % (self.timestamp)