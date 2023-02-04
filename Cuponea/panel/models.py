from django.db import models
from redeem import models as redeem
from django.contrib.auth import get_user_model

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
    
class BusinessUserPermission(models.Model):
    PERM_LEVELS = (
        (1, 'Regular Staff'),
        (2, 'Managers'),
        (3, 'Business Admin'),
        #Ensure this is studied enough before launching to test/prod with these options
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
    #Check if user_affected would work with get_user_model()
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='business_user_admin_permissions')
    
    class Meta:
        verbose_name_plural = 'business user permissions'
    def __str__(self):
        return "User #%s to User #%s - %s" % (self.user_admin.id, self.user_affected.id, self.status)
    
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
    
class TimePurchaseHistory(models.Model):
    timestamp = models.DateTimeField('time purchase history timestamp', auto_now_add=True)
    time_purchased = models.IntegerField('time purchased')
    remarks = models.CharField('time purchase history remarks', max_length=100, blank=True)
    user_admin = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='time_purchase_history')
    
    class Meta:
        verbose_name_plural = 'time purchase history'
    def __str__(self):
        return "Transaction #%s by User #%s" % (self.id, self.user_admin.id)

#Is there anything else we should add here?
class StaffInfo(models.Model):
    #first name and last name are not included here because we'll make the
    # staff creation view make it mandatory for staff members in the user model
    #Also, business_staff flag is NOT needed.
    staff_member = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name='staff_member_info')
    branch = models.ForeignKey(redeem.Branch, models.SET_NULL, null=True, related_name='branch_staff_info')
    remarks = models.CharField('staff info remarks', max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = 'staff info'
        #Check if this is needed elsewhere
        unique_together = (('staff_member', 'branch'),)
    def __str__(self):
        return "User #%s Staff Info" % (self.staff_member.id)