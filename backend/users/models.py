from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 

# AbstractUser Django's existing user functionality and it allows us to add additional fields.
from django.contrib.auth.models import AbstractUser

# Utilities
from datetime import date

class User(AbstractUser):
    is_email_verified = models.BooleanField(default = False)

# Used by the Fitness Profile Class to allow users to have multiple fitness goals.
class FitnessGoals(models.Model):
    FITNESS_GOALS = [
        # Body composition
        ("build_muscle", "Build muscle"),
        ("lose_weight", "Lose weight"),
        ("lose_body_fat", "Lose body fat"),
        ("gain_weight", "Gain weight"),
        ("maintain_weight", "Maintain weight"),
        ("body_recomposition", "Body recomposition"),

        # Strength and muscle development
        ("increase_strength", "Increase strength"),
        ("increase_muscle_size", "Increase muscle size"),
        ("improve_muscular_endurance", "Improve muscular endurance"),
        ("improve_power", "Improve explosive power"),

        # Cardiovascular fitness
        ("improve_cardio", "Improve cardiovascular fitness"),
        ("improve_stamina", "Improve stamina"),
        ("improve_endurance", "Improve endurance"),
        ("improve_running", "Improve running performance"),

        # Mobility and physical health
        ("improve_flexibility", "Improve flexibility"),
        ("improve_mobility", "Improve mobility"),
        ("improve_balance", "Improve balance"),
        ("improve_posture", "Improve posture"),
        ("improve_general_health", "Improve general health"),
        ("improve_heart_health", "Improve cardiovascular health"),

        # Athletic performance
        ("improve_athletic_performance", "Improve athletic performance"),
        ("improve_sports_performance", "Improve sports performance"),
        ("improve_recovery", "Improve recovery"),

        # General fitness
        ("build_consistency", "Build workout consistency"),
        ("maintain_fitness", "Maintain fitness"),
        ("increase_energy", "Increase daily energy levels"),
    ]

    name = models.CharField(choices = FITNESS_GOALS, max_length = 50)

    def __str__(self):
        return self.get_name_display()

class FitnessProfile(models.Model):

    GENDERS = [
        ("female","Female"),
        ("male","Male")
    ]

    PHYSICAL_LIMITATIONS = [
        ("none", "No known physical limitations"),
        ("mobility", "Mobility limitations"),
        ("joint_problems", "Joint problems"),
        ("back_problems", "Back problems"),
        ("neck_problems", "Neck problems"),
        ("muscle_injuries", "Muscle injuries"),
        ("ligament_injuries", "Ligament injuries"),
        ("tendon_injuries", "Tendon injuries"),
        ("chronic_pain", "Chronic pain"),
        ("arthritis", "Arthritis"),
        ("cardiovascular", "Cardiovascular conditions"),
        ("respiratory", "Respiratory conditions"),
        ("neurological", "Neurological conditions"),
        ("balance_coordination", "Balance or coordination difficulties"),
        ("visual_impairment", "Visual impairment"),
        ("hearing_impairment", "Hearing impairment"),
        ("limb_difference", "Limb difference or amputation"),
        ("pregnancy_postpartum", "Pregnancy or postpartum considerations"),
        ("other", "Other physical limitations"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    WORKOUT_TYPES = [
        # Strength and resistance training
        ("bodybuilding", "Bodybuilding"),
        ("powerlifting", "Powerlifting"),
        ("weightlifting", "Olympic Weightlifting"),
        ("strength_training", "General Strength Training"),
        ("hypertrophy", "Hypertrophy Training"),
        ("strongman", "Strongman"),

        # Bodyweight training
        ("calisthenics", "Calisthenics"),
        ("street_workout", "Street Workout"),
        ("gymnastics", "Gymnastics"),

        # Functional and hybrid fitness
        ("hyrox", "HYROX"),
        ("crossfit", "CrossFit"),
        ("functional_fitness", "Functional Fitness"),
        ("circuit_training", "Circuit Training"),
        ("hiit", "High-Intensity Interval Training (HIIT)"),

        # Cardiovascular and endurance
        ("running", "Running"),
        ("cycling", "Cycling"),
        ("swimming", "Swimming"),
        ("rowing", "Rowing"),
        ("triathlon", "Triathlon"),
        ("endurance_training", "Endurance Training"),

        # Mobility and flexibility
        ("yoga", "Yoga"),
        ("pilates", "Pilates"),
        ("mobility_training", "Mobility Training"),
        ("stretching", "Stretching"),

        # Sports and athletic development
        ("athletic_training", "Athletic Performance Training"),
        ("sports_conditioning", "Sports Conditioning"),
        ("martial_arts", "Martial Arts"),
        ("boxing", "Boxing"),
        ("combat_sports", "Combat Sports"),
        ("speed_agility", "Speed and Agility Training"),

        # General fitness
        ("general_fitness", "General Fitness"),
        ("weight_loss_training", "Weight Loss Training"),
    ]

    WORKOUT_FREQUENCY = [
        (1, "1 day per week"),
        (2, "2 days per week"),
        (3, "3 days per week"),
        (4, "4 days per week"),
        (5, "5 days per week"),
        (6, "6 days per week"),
        (7, "7 days per week"),
    ]

    ATHLETIC_EXPERIENCE = [
        ("beginner","Beginner"),
        ("moderate","Moderate"),
        ("advanced","Advanced")
    ]

    WORKOUT_DURATIONS = [
        (30, "30 minutes"),
        (45, "45 minutes"),
        (60, "60 minutes"),
        (75, "75 minutes"),
        (90, "90 minutes"),
        (105, "105 minutes"),
        (120, "120 minutes"),
        (135, "135 minutes"),
        (150, "150 minutes"),
        (165, "165 minutes"),
        (180, "180 minutes"),
        (195, "195 minutes"),
        (200, "200 minutes"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        blank = False,
        null = False
    )

    gender = models.CharField(choices = GENDERS , null = False, blank = False, max_length = 50)
    height_cm = models.PositiveSmallIntegerField(validators = [MinValueValidator(50),MaxValueValidator(250)])
    date_of_birth = models.DateField(null = False, blank = False)
    physical_limitations = models.CharField(choices = PHYSICAL_LIMITATIONS, null = True, blank = True, max_length = 50)
    physical_limitations_more_info = models.TextField(null = True, blank = True)
    # A Many-to-Many relationship is appropriate because one FitnessProfile can have multiple goals, and the same goal can be shared by multiple FitnessProfiles.
    fitness_goal = models.ManyToManyField(FitnessGoals, related_name = "all_goals")
    workout_preference = models.CharField(choices = WORKOUT_TYPES, blank = False, null = False, max_length = 50)
    athletic_experience = models.CharField(choices = ATHLETIC_EXPERIENCE, blank = False, null = False, max_length = 50)
    workouts_per_week = models.PositiveSmallIntegerField(choices = WORKOUT_FREQUENCY, blank = False, null = False)
    workout_duration = models.PositiveSmallIntegerField(choices = WORKOUT_DURATIONS)

    @property
    def age(self):
        today = date.today()

        age = today.year - self.date_of_birth.year

        # Prevents rounding up an age
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        
        return age