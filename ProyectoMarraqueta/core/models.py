from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models

""" Base User Models """

class Role(models.TextChoices):
    ADMIN = "ADM", 'Admin'
    STUDENT = "STU", 'Student'
    PROFESSOR = "PRO", 'Professor'
    ACADEMIC = "ACA", 'Academic'
    EXTERNAL = "EXT", 'External'
    STAFF = "STA", 'Staff'
    GUARD = "GUA", 'Guard'


class User(AbstractUser):
    AbstractUser.username = models.CharField(verbose_name="Nombre", max_length=25, null=False, default="A")
    last_name = models.CharField(verbose_name="Apellido", max_length=25, null=None)
    run = models.PositiveBigIntegerField(
        verbose_name="RUN", 
        null=True, 
        unique=True,
        error_messages={
            'unique': "Ese RUN ya se encuentra registrado."
        })

class UsmUser(User):
    AbstractUser.email = models.EmailField(
        verbose_name="Email USM", 
        max_length=25, 
        null=None, 
        unique=True,
        error_messages={
            'unique': "Ese correo ya se encuentra registrado."
        })
    usm_role = models.PositiveBigIntegerField(
        verbose_name="ROL USM", 
        null=True, 
        default=None,
        error_messages={
            'unique': "Ese ROL ya se encuentra regisrado."
        })

class OtherUser(User):
    AbstractUser.email = models.EmailField(
        verbose_name="Email", 
        max_length=25, 
        null=None, 
        unique=True,
        error_messages={
            'unique': "Ese correo ya se encuentra registrado."
        })


""" Derivative user models """

class Student(UsmUser):
    career = models.CharField("Carrera", max_length=20, default=None, null=True) #TODO CHANGE CAREER TO CHOICES FIELD
    user_type = models.CharField(choices=Role.choices, default=Role.STUDENT, max_length=3)

    def __str__(self):
        return "Estudiante " + str(self.run)
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

class Professor(UsmUser):
    user_type = models.CharField(choices=Role.choices, default=Role.PROFESSOR, max_length=3)
    department = models.CharField("Departamento", max_length=20, default=None, null=True)
    
    def __str__(self):
        return "Profesor " + str(self.run)
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

class Academic(OtherUser):
    user_type = models.CharField(choices=Role.choices, default=Role.ACADEMIC, max_length=3)
    connection = models.CharField("Conexión con USM", max_length=100, default=None, null=True)

    def __str__(self):
        return "Academico " + str(self.run)
    
    class Meta:
        verbose_name = "Academico"
        verbose_name_plural = "Academicos"

class External(OtherUser):
    user_type = models.CharField(choices=Role.choices, default=Role.EXTERNAL, max_length=3)
    connection = models.CharField("Conexión con USM", max_length=100, default=None, null=True)

    def __str__(self):
        return "Externo " + str(self.run)
    
    class Meta:
        verbose_name = "Externo"
        verbose_name_plural = "Externos"

class Staff(OtherUser):
    user_type = models.CharField(choices=Role.choices, default=Role.STAFF, max_length=3)
    charge = models.CharField("Cargo en USM", max_length=40, default=None, null=True)
    def __str__(self):
        return "Staff " + str(self.run)
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

class Guard(OtherUser):
    user_type = models.CharField(choices=Role.choices, default=Role.GUARD, max_length=3)
    def __str__(self):
        return "Guardia " + str(self.run)
    
    class Meta:
        verbose_name = "Guardia"
        verbose_name_plural = "Guardias"
    



""" Non Human Models """

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
    bicy_user = models.ForeignKey("User", on_delete=models.CASCADE)
    is_saved = models.BooleanField("Am I saved?", default=False)

    image = models.ImageField(upload_to="uploads/", default=None, null=True)

class KeyChain(models.Model):
    uuid = models.CharField("UUID", default=None, max_length=12)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

class BicycleHolder(models.Model):
    def __str__(self):
        return f"Holder N. {self.pk}"

    def save(self, *args, **kwargs):
        """
            This code below, adds or deletes BicycleHolder slots when saving the instance.
        """
        self_slots = self.tracker["slots"]
        if len(self_slots) == 0:
            for i in range(self.capacity):
                self_slots.append(0)
        else:
            delta_capacity = self.capacity - len(self_slots)
            if delta_capacity > 0:
                for i in range(delta_capacity):
                    self_slots.append(0)
            else:
                self_slots = self_slots[:self.capacity]
        
        super().save(*args, **kwargs)   
        print(f"Holder.{self.pk} modified, slots: {self_slots}")

    def check_bicycle(self, bicycle):
        """Check if the given Bicycle is in the slots arr

        Args:
            Bicycle (core.models.Bicycle): _description_

        Returns:
            Int: not -1 if exists. -1 if not exists.
        """
        bicycle_pk = bicycle.pk
        self_slots = self.tracker['slots']

        try:
            return self_slots.index(bicycle_pk)
        except ValueError:
            return -1

    def add_bicycle(self, bicycle):
        """Add a bicycle instance's PK to the slots arr.

        Args:
            Bicycle (core.models.Bicycle): instance of core.Bicycle model.

        Returns:
            (Int, Int/None): Tuple(Status Code, Empty_Place's index). Status code: 0(success), 1(Bicycle not instance of Bicycle), 2(No empty place)
        """
        self_slots = self.tracker["slots"]
        if isinstance(bicycle, Bicycle): # check if bicycle belongs to Bicycleclass
            try:
                empty_place = self_slots.index(0)
                self_slots[empty_place] = bicycle.pk
                self.save()
                return (0, empty_place) 
            except ValueError:
                return (2, None)
        else:
            return (1, None)

    def del_bicycle(self, bicycle):
        """Deletes a bicycle from the BicycleHolder

        Args:
            bicycle_pk (Int): The primary key of a core.Bicycle model

        Returns:
            Int: Available index OR -1 if bicycle not in slots
        """
        self_slots = self.tracker["slots"]

        bicycle_pk = bicycle.pk
        if type(bicycle_pk) == type(0):  # Check if the type of bicycle_pk is int
            try:
                bicycle_index = self_slots.index(bicycle_pk)
                self_slots[bicycle_index] = 0
                self.save()
                return bicycle_index
            except ValueError:
                return -1

    BUILDING_SJ_CHOICES = {
        "K": "K",
        "A": "A",
        "B": "B",
        "C": "C",
        "E": "E"
    }

    def get_default_json():
        return {"slots": []}

    tracker = models.JSONField(default=get_default_json)
    capacity = models.SmallIntegerField("Capacity", default=1, null=False)
    location = models.CharField("Location", max_length=30)
    nearest_building = models.CharField("Nearest building", max_length=1, choices=BUILDING_SJ_CHOICES)

class EspModule(models.Model):
    #ip_address = models.GenericIPAddressField(protocol='IPv4', default=None, null=True)
    ip_address = models.CharField(max_length=15, null=False, default="0.0.0.0")
    latest_online = models.DateTimeField("Lastest online", null=True)
    bicycleholder = models.OneToOneField(BicycleHolder, on_delete=models.CASCADE, default=None)
