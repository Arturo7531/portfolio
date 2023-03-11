# Cuponea panel app database model file.
# This app is still in development, and is not yet implemented in the front end.

# First, we import necessary packages and functions
from django.db import models
from redeem import models as redeem
from django.contrib.auth import get_user_model

# This class allows us to keep track of all offers the business has created
class OfferHistory(models.Model):
    ACTIONS = (
        ('ADD', 'New offer added'),
        ('MOD', 'Offer modified'),
        ('CXL', 'Offer cancelled')
        )
    timestamp = models.DateTimeField('offer history timestamp', auto_now_add=True)
    action = models.CharField('offer history action', max_length=3, choices=ACTIONS)
    time_used = models.IntegerField('offer history time used')
    remarks = models.CharField('offer history remarks', max_length=100, blank=True)
    offer = models.ForeignKey(redeem.Offer, models.CASCADE, related_name='offer_history')
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='offer_history')
    
    class Meta:
        verbose_name_plural = 'offer history'
    def __str__(self):
        return "%s - %s - %s" % (self.offer.business.name, self.action, self.offer.name)
    
# This class sets the permissions for each user in the business
class BusinessUserPermission(models.Model):
    PERM_LEVELS = (
        (1, 'Regular Staff'),
        (2, 'Managers'),
        (3, 'Business Admin'),
        )
    STATUS = (
        ('ADD', 'New staff member added'),
        ('MOD', 'Staff member modified'),
        ('DEA', 'Staff member deactivated')
        )
    timestamp = models.DateTimeField('business user permission timestamp', auto_now_add=True)
    status = models.CharField('business user permission status', max_length=3, choices=STATUS)
    permission = models.PositiveSmallIntegerField('business user permission', choices=PERM_LEVELS)
    remarks = models.CharField('offer history remarks', max_length=100, blank=True)
    user_affected = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='business_affected_user_permissions')
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='business_user_admin_permissions')
    
    class Meta:
        verbose_name_plural = 'business user permissions'
    def __str__(self):
        return "User #%s to User #%s - %s" % (self.user_admin.id, self.user_affected.id, self.status)
    
# This class allows us to keep track of all the branches the business has created
class BusinessBranchHistory(models.Model):
    STATUS = (
        ('ADD', 'New branch added'),
        ('MOD', 'Branch modified'),
        ('DEA', 'Branch deactivated')
        )
    timestamp = models.DateTimeField('business branch history timestamp', auto_now_add=True)
    status = models.CharField('business branch status', max_length=3, choices=STATUS)
    remarks = models.CharField('business branch history remarks', max_length=100, blank=True)
    branch = models.ForeignKey(redeem.Branch, models.SET_NULL, null=True, related_name='business_branch_history')
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='business_branch_history')
    
    class Meta:
        verbose_name_plural = 'business branch history'
    def __str__(self):
        return "%s - %s - %s" % (self.branch.business.name, self.branch.name, self.status)
    
# This class allows us to keep track of all the time purchases the business has made.
# The model of the business is to sell timeslots in the front end, and then use the
# time purchased to create offers in the backend.
class TimePurchaseHistory(models.Model):
    timestamp = models.DateTimeField('time purchase history timestamp', auto_now_add=True)
    time_purchased = models.IntegerField('time purchased')
    remarks = models.CharField('time purchase history remarks', max_length=100, blank=True)
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='time_purchase_history')
    
    class Meta:
        verbose_name_plural = 'time purchase history'
    def __str__(self):
        return "Transaction #%s by User #%s" % (self.id, self.user_admin.id)

# This class allows for the creation of staff info for each staff member.
# This is still in development, and is not yet implemented in the front end.
class StaffInfo(models.Model):
    staff_member = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='staff_member_info')
    branch = models.ForeignKey(redeem.Branch, models.SET_NULL, null=True, related_name='branch_staff_info')
    remarks = models.CharField('staff info remarks', max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = 'staff info'
        unique_together = (('staff_member', 'branch'),)
    def __str__(self):
        return "User #%s Staff Info" % (self.staff_member.id)