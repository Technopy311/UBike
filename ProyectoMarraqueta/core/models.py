from django.contrib.auth.models import AbstractUser
from django.db import models


class BicyUser(AbstractUser):

    USER_TYPE_CHOICES = {
        "STU": "Student",
        "PRO": "Professor",
        "ACA": "Academic",
        "EXT": "External",
        "STA": "Staff",
    }

    name = models.CharField(verbose_name="Nombre", max_length=25, null=None)
    last_name = models.CharField(verbose_name="Apellido", max_length=25, null=None)
    usm_email = models.EmailField(
        verbose_name="Email USM", 
        max_length=25, 
        null=None, 
        unique=True,
        error_messages={
            'unique': "Ese correo ya se encuentra registrado."
        })
    run = models.PositiveBigIntegerField(
        verbose_name="RUN", 
        null=None, 
        unique=True, 
        error_messages={
            'unique': "Ese RUN ya se encuentra registrado."
        })
    usm_role = models.PositiveBigIntegerField(
        verbose_name="ROL USM", 
        null=True, 
        default=None,
        error_messages={
            'unique': "Ese ROL ya se encuentra regisrado."
        })
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default="STU", max_length=3)

    def is_student(self):
        return self.user_type == "STU"
    def is_professor(self):
        return self.user_type == "PRO"
    def is_academic(self):
        return self.user_type == "ACA"
    def is_external(self):
        return self.user_type == "EXT"
    def is_staff(self):
        return self.user_type == "STA"


class Bicycle(models.Model):
    BIKES_CHOICES = {
        "RB": "Road Bike",
        "CCB": "Cyclo-cross Bike",
        "GB": "Grave Bike",
        "TTB": "Time Trial Bike",
        "TB": "Touring Bike",
        "FB": "Folding Bike",
        "BMX": "BMX",
        "EB": "Electric Bike"
    }

    
    model = models.CharField("Bicycle model", max_length=100, null=False)
    colour = models.CharField("Bicycle color", max_length=100, null=False)
    bike_type = models.CharField(
        max_length=3,
        choices=BIKES_CHOICES,
        default="RB",
        null=False
    )
    bicy_user = models.ForeignKey("BicyUser", on_delete=models.CASCADE)


class Guard(models.Model):
    #Inherits Django user
    name = models.CharField("Name", max_length=20, null=False),
    last_name = models.CharField("Lastname", max_length=30, null=False),
    run = models.PositiveIntegerField("RUN", null=False)


class KeyChain(models.Model):
    uuid = models.PositiveBigIntegerField("UUID", default=None, null=True)
    user = models.ForeignKey("BicyUser", on_delete=models.CASCADE)



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
    def check_bicycle(cls, Bicycle):
        """Check if the given Bicycle is in the slots arr

        Args:
            Bicycle (core.models.Bicycle): _description_

        Returns:
            Int: 0 if exists. 1 if not exists. -1 if Bicycle.pk not integer.
        """
        try:
            if Bicycle.pk in cls.slots():
                return 0
            else:
                return 1
        except ValueError:
            return -1
        

    @classmethod
    def add_bicycle(cls, Bicycle):
        """Add a bicycle instance's PK to the slots arr.

        Args:
            Bicycle (core.models.Bicycle): instance of core.Bicycle model.

        Returns:
            Int: 0 if success. 1 if Bicycle not instance of core.Bicycle. 2 if no space.
            
        """

        if Bicycle.isinstance(Bicycle):
            try:
                empty_place = cls.slots.index(0)
            except ValueError:
                return 2
            
            cls.slots[empty_place] = Bicycle.pk
            return 0
        else:
            return 1


    @classmethod
    def del_bicycle(cls, bicycle_pk):
        """Deletes a bicycle from the BicycleHolder

        Args:
            bicycle_pk (Int): The primary key of a core.Bicycle model

        Returns:
            Int: 0 if bicycle deleted succesfully
            Int: 1 if bicycle_pk is not Int
            Int: 2 if bicycle_pk is not in slots
        """

        if type(bicycle_pk) == type(0):  # Check if the type of bicycle_pk is int
            try:
                bicycle_index = cls.slots.index(bicycle_pk)
            except ValueError:
                return 2
            
            cls.slots[bicycle_index] = 0
            return 0
        else:
            return 1
        
        


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


