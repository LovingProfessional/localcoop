from django.db import models

#This integer represents a single subscription
WHOLESUBSCRIPTION = 60

# Create your models here.
class Group(models.Model):
    id = models.AutoField(primary_key=True) #Not sure if needed
    self.nonWholeGroupSubscriptions = set()

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
        for coop, totalshares in groupSubscriptions.iteritems():
            if not totalshares % 60 == 0:
                self.nonWholeGroupSubscriptions.add(coop)
                
class CoopUser(models.Model):
    group = models.ForeignKey('Group')
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone = CharField(max_length=10)
    wesid = CharField(max_length=6)
    email = EmailField(max_length=30)

    def get_subscriptions(self):
        return Subscription.objects.filter(coopuser=self)

class Coop(models.Model):
    id = models.AutoField(primary_key=True)
    name = CharField(max_length=50)

class Subscription(models.Model):
    shares = models.IntegerField()
    coopuser = models.ForeignKey('CoopUser')
    coop = models.ForeignKey('Coop')

