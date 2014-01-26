from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#This integer represents a single subscription
WHOLESUBSCRIPTION = 60

# All App models here.
class Group(models.Model):
    id = models.AutoField(primary_key=True) #Not sure if needed
    nonWholeGroupSubscriptions = set()

    def get_members(self):
        return CoopUser.objects.filter(group=self)

    def validate_share_ammounts(self):
        groupSubscriptions = {} #Map coops to total shares in the group
        for coop in Coop.objects.all():
            groupSubscriptions[coop] = 0
        for member in self.get_members():
            for memberSubscription in member.get_subscriptions():
                groupSubscriptions[memberSubscription.coop] += memberSubscription.shares
        self.nonWholeGroupSubscriptions = set()
        for coop, totalshares in groupSubscriptions.items():
            if not totalshares % WHOLESUBSCRIPTION == 0:
                self.nonWholeGroupSubscriptions.add(coop)

    def __str__(self):
        s = "Group( "
        for m in self.get_members():
            s += m.firstname + m.lastname + ','
        s = s[:-1] + ')'
        return s
admin.site.register(Group)
                
class CoopUser(models.Model):
    user = models.OneToOneField(User)
    group = models.ForeignKey(Group)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    wesid = models.CharField(max_length=6)
    email = models.EmailField(max_length=30)

    def get_subscriptions(self):
        return Subscription.objects.filter(coopuser=self)

    def __str__(self):
        return self.firstname + self.lastname
admin.site.register(CoopUser)

class Coop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return name
admin.site.register(Coop)

class Subscription(models.Model):
    shares = models.IntegerField()
    coopuser = models.ForeignKey('CoopUser')
    coop = models.ForeignKey('Coop')

    def __str__(self):
        return str(shares) + " shares of " + str(coop) + " for " + str(coopuser)
admin.site.register(Subscription)

