# Cuponea redeem app database model file.

# First, we import necessary packages and functions
import uuid
from django.db import models
from django.contrib.auth import get_user_model


# This class represents a food item in the catalogue
class CatalogueFoodType(models.Model):
    name = models.CharField('food type name', max_length=30)
    visible = models.BooleanField('food type visibility', default=False)
    
    class Meta:
        verbose_name = 'food type'
        verbose_name_plural = 'food types'
    def __str__(self):
        return self.name

def business_logo_directory_path(instance, filename):
    return 'logos/{0}/{1}'.format(instance.name, filename)


# This class represents the relation between a business and a food type. 
# The purpose of this class is to provide a many-to-many relationship between these two classes.
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
    
    class Meta:
        verbose_name_plural = 'businesses'
    def __str__(self):
        return self.name


# A junction table for linking Businesses with FoodTypes
class FoodTypeJunction(models.Model):
    business = models.ForeignKey(Business, models.PROTECT, related_name='food_type_junctions')
    food_type = models.ForeignKey(CatalogueFoodType, models.PROTECT, related_name='food_type_junctions')
        
    class Meta:
        verbose_name_plural = 'food type junctions'
        unique_together = (('business', 'food_type'),)
    def __str__(self):
        return "%s - %s" % (self.business.name, self.food_type.name)
   
# This class represents a political division, a subdivision of a larger political entity.
# The purpose of this being to segment our customers by location.
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


# This class represents the information of a business branch.
# This model also links staff members with their branch information through a many-to-many relationship.
class Branch(models.Model):
    STATUS = (
        ('ACT', 'Branch active'),
        ('INA', 'Branch inactive')
        )
    name = models.CharField('branch name', max_length=60)
    address = models.CharField('branch address', max_length=70)
    website = models.URLField('branch website URL', max_length=200, blank=True)
    phone = models.CharField('branch phone number', max_length=8, blank=True)
    description = models.CharField('branch description', max_length=300)
    latitude = models.FloatField('branch latitude')
    longitude = models.FloatField('branch longitude')
    status = models.CharField('business branch status', max_length=3, choices=STATUS)
    corr = models.ForeignKey(CataloguePoliticalDivision, on_delete=models.PROTECT, related_name='branches')
    business = models.ForeignKey(Business, models.CASCADE, related_name='branches')
    staff_info = models.ManyToManyField(get_user_model(), through='panel.StaffInfo')
    
    class Meta:
        verbose_name_plural = 'branches'
    def __str__(self):
        return '%s %s' % (self.business.name, self.name)


# This class represents the schedule of a business branch.
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
    
    class Meta:
        verbose_name_plural = 'branch schedules'
    def __str__(self):
        return '%s - %s - DOW %s' % (self.branch.business.name, self.branch.name, self.week_day)
    
    
def offer_image_directory_path(instance, filename):
    return 'offers/{0}/{1}'.format(instance.branch.business.id, filename)


# This class represents an offer, including each offer's details, type, and schedule.
# It also links the offer to the business branch that is offering it.
# Finally, since this is a heavily transacted class, it contains indexes for the most common queries.
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
    name = models.CharField('offer name', max_length=50)
    description = models.CharField('offer description', max_length=100)
    redemption_type = models.PositiveSmallIntegerField('offer redemption type', choices=RED_TYPES)
    image_path = models.ImageField('item image path', upload_to=offer_image_directory_path, blank=True)
    start_dtm = models.DateTimeField('offer start datetime')
    end_dtm = models.DateTimeField('offer end datetime')
    original_value = models.DecimalField('offer original value', max_digits=5, decimal_places=2, null=True, blank=True)
    discounted_value = models.DecimalField('offer discounted value', max_digits=5, decimal_places=2, null=True, blank=True)
    cxl_type = models.PositiveSmallIntegerField('offer cancellation type', choices=CXL_TYPES, default=0)
    branch = models.ManyToManyField(Branch, through='BranchOfferJunction')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='offers')

    class Meta:
        verbose_name_plural = 'offers'
        indexes = [
            models.Index(fields=['start_dtm'], name='start_dtm_idx'),
            models.Index(fields=['end_dtm'], name='end_dtm_idx'),
            models.Index(fields=['start_dtm', 'end_dtm'], name='active_offers_idx'),
        ]
    def __str__(self):
        return '%s - %s' % (self.business.name, self.name)


# This class represents the junction between a business branch and an offer.
class BranchOfferJunction(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_offer_junctions')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='branch_offer_junctions')
    
    class Meta:
        verbose_name_plural = 'branch offer junctions'
        unique_together = (('branch', 'offer'),)
    def __str__(self):
        return "%s - %s - %s" % (self.branch.business.name, self.branch.name, self.offer.name)


# This class represents a Coupon redemption.
# It links the coupon to the user that redeemed it, the offer that was redeemed, and the branch that issued it.
# It also contains an index for the most common query.
class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    use_dtm = models.DateTimeField('coupon use datetime', auto_now=True)
    offer = models.ForeignKey(Offer, models.CASCADE, related_name= 'coupons')
    branch = models.ForeignKey(Branch, models.CASCADE, related_name='coupons')
    user = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='coupons_user')
    
    class Meta:
        verbose_name_plural = 'coupons'
        indexes = [
            models.Index(fields=['user_id', 'offer_id'], name='user_invalid_attempt_idx'),
        ]

    def __str__(self):
        return '%s - Coupon # %s' % (self.offer.business.name, self.id)


# This class represents every time a user queries the system for offers. 
# It stores the user's location and the time of the query.
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