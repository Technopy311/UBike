from django.db import models
from django.contrib.auth.models import AbstractUser

#class BicyUser(AbstractUser):#userbastrac
    #inherits Django User
    #pass

class BicyUser(models.Model):
    #dummy Model
    pass


class Bicycle(models.Model):
    ROADBIKE = "RB"
    CYCLOCROSS = "CCB"
    GRAVEL = "GB"
    TIMETRIAL = "TTB"
    TOURING = "TB"
    FOLDING = "FB"
    BMX = "BMX"
    EBIKE = "EB"
    
    BIKES_CHOICES = {
        ROADBIKE: "Road Bike",
        CYCLOCROSS: "Cyclo-cross Bike",
        GRAVEL: "Grave Bike",
        TIMETRIAL: "Time Trial Bike",
        TOURING: "Touring Bike",
        FOLDING: "Folding Bike",
        BMX: "BMX",
        EBIKE: "Electric Bike"
    }

    
    model = models.CharField("Bicycle model", max_length=100, null=False)
    colour = models.CharField("Bicycle color", max_length=100, null=False)
    bike_type = models.CharField(
        max_length=3,
        choices=BIKES_CHOICES,
        default=ROADBIKE,
        null=False
    )
    bicy_user = models.ForeignKey("BicyUser", on_delete=models.CASCADE)


class Guard(models.Model):
    #Inherits Django user
    name = models.CharField("Name", max_length=20, null=False),
    last_name = models.CharField("Lastname", max_length=30, null=False),
    run = models.PositiveIntegerField("RUN", null=False)


class BicycleHolder(models.Model):
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        """
            This code below, adds or deletes BicycleHolder slots when saving the instance.
        """
        if len(self.slots) == 0:
            for i in range(self.capacity):
                self.slots.append(0)
        else:
            delta_capacity = self.capacity - len(self.slots)
            if delta_capacity > 0:
                for i in range(delta_capacity):
                    self.slots.append(0)
            else:
                self.slots = self.slots[:self.capacity]


    @classmethod
    def add_bicycle(cls, Bicycle):
        """Add a bicycle instance to the slots arr

        Args:
            Bicycle (_core.Bicycle_): instance of core.Bicycle model

        Returns:
            Bool: 0 if succes; 1 if Bicycle is not instance of core.Bicycle
        """

        if Bicycle.isinstance(Bicycle):
            empty_place = cls.slots.index(0)
            cls.slots[empty_place] = Bicycle
            return False
        else:
            return True


    BUILDING_SJ_CHOICES = {
        "K": "K",
        "A": "A",
        "B": "B",
        "C": "C",
        "E": "E"
    }
    slots = []
    capacity = models.PositiveSmallIntegerField("Capacity", default=1, null=False)
    location = models.CharField("Location", max_length=30)
    nearest_building = models.CharField("Nearest building", max_length=1, choices=BUILDING_SJ_CHOICES)
    nearest_guard = models.ForeignKey("Guard", on_delete=models.CASCADE, null=True, default=None)


class KeyChain(models.Model):
    uuid = models.PositiveBigIntegerField("UUID", default=None, null=True)
    user = models.ForeignKey("BicyUser", on_delete=models.CASCADE)

