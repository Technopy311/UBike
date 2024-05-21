from django.test import TestCase

from . import models as core_models
from django.utils import timezone

class UserCreationTests(TestCase):

    def test_create_student_user(self):
        career = "ICTEL"
        dummyUser = core_models.Student(career=career)
        self.assertIs(dummyUser.career, career)
        self.assertIs(dummyUser.user_type, core_models.Role.STUDENT)
    
    def test_create_professor_user(self):
        departamento = "ICMAT"
        dummyProfessor = core_models.Professor(department=departamento)
        self.assertIs(dummyProfessor.department, departamento)
        self.assertIs(dummyProfessor.user_type, core_models.Role.PROFESSOR)
    
    def test_create_academic_user(self):
        connection = "Atacama Desert"
        dummyAcademic = core_models.Academic(connection=connection)
        self.assertIs(dummyAcademic.connection, connection)
        self.assertIs(dummyAcademic.user_type, core_models.Role.ACADEMIC)

    def test_create_staff_user(self):
        charge = "Secretaria"
        dummyStaff = core_models.Staff(charge=charge)
        self.assertIs(dummyStaff.user_type, core_models.Role.STAFF)
        self.assertIs(dummyStaff.charge, charge)
    
    def test_create_guard_user(self):
        dummyGuard = core_models.Guard()
        self.assertIs(dummyGuard.user_type, core_models.Role.GUARD)


class NonHumanCreationTests(TestCase):

    def test_bicycle_creation(self):
        department = "DFIS"
        dummyUser = core_models.Professor(department=department)
        dummyBicycle = core_models.Bicycle(
            model="TRX",
            colour="Magenta",
            bike_type = "TTB",
            bicy_user=dummyUser,
        )

        self.assertIs(dummyBicycle.model, "TRX")
        self.assertIs(dummyBicycle.colour, "Magenta")
        self.assertIs(dummyBicycle.bike_type, "TTB")
        self.assertIs(dummyBicycle.bicy_user, dummyUser)
    
    def test_keychain_creation(self):
        uuid=123456789
        dummyUser = core_models.Guard()
        dummyKeychain = core_models.KeyChain(user=dummyUser, uuid=uuid)
        
        self.assertIs(dummyKeychain.uuid, uuid)
        self.assertIs(dummyKeychain.user, dummyUser)
    
    def test_bicycleholder_creation(self):
        dummyGuard = core_models.Guard()

        capacity=5
        location="LOL!#$%"
        nearest_building = "C"
        dummyHolder = core_models.BicycleHolder(
            capacity=capacity,
            location=location,
            nearest_building=nearest_building,
            nearest_guard=dummyGuard
        )
        self.assertIs(dummyHolder.capacity,5)
        self.assertIs(dummyHolder.location, location)
        self.assertIs(dummyHolder.nearest_building, nearest_building)
        self.assertIs(dummyHolder.nearest_guard, dummyGuard)
    
    def test_espmodule_creation(self):
        dummyGuard = core_models.Guard()

        capacity=5
        location="LOL!#$%"
        nearest_building = "C"
        dummyHolder = core_models.BicycleHolder(
            capacity=capacity,
            location=location,
            nearest_building=nearest_building,
            nearest_guard=dummyGuard
        )
        
        ip_address = "255.255.255.255"
        latest_online = timezone.now()
        
        dummyModule = core_models.EspModule(
            ip_address=ip_address,
            latest_online=latest_online,
            bicycleholder=dummyHolder
        )

        self.assertIs(dummyModule.ip_address, ip_address)
        self.assertIs(dummyModule.latest_online, latest_online)
        self.assertIs(dummyModule.bicycleholder, dummyHolder)