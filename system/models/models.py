import calendar
from datetime import date
# from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from conf.models import District, County, SubCounty, Parish, Product, Crop, ProductVariation
from system.models.modelmixin import TimeStampMixin
from system.models.land import land_upload_path

User = settings.AUTH_USER_MODEL


class Cooperative(TimeStampMixin):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='cooperatives/', null=True, blank=True)
    code = models.CharField(max_length=150, unique=True, null=True, blank=True)
    coop_abbreviation = models.CharField(max_length=150, unique=True, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    contact_person_name = models.CharField(max_length=150)
    product = models.ManyToManyField(Product, blank=True)
    contribution_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    shares = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_active = models.BooleanField(default=0)
    send_message = models.BooleanField(default=0,
                                       help_text='If not set, the cooperative member will not receive SMS\'s when sent.')
    date_joined = models.DateField()
    sms_api_url = models.CharField(max_length=255, null=True, blank=True)
    sms_api_token = models.CharField(max_length=255, null=True, blank=True)
    payments_account = models.CharField(max_length=255, null=True, blank=True)
    payments_token = models.CharField(max_length=255, null=True, blank=True)
    payments_authentication = models.CharField(max_length=255, null=True, blank=True)
    system_url = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cooperative'

    def __unicode__(self):
        return self.name


class FarmerGroup(TimeStampMixin):
    name = models.CharField(max_length=255)
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=150, unique=True, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    contact_person_name = models.CharField(max_length=150)
    contact_person_number = models.CharField(max_length=150)
    product = models.ManyToManyField(Product, blank=True)
    contribution_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    shares = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_active = models.BooleanField(default=0)
    send_message = models.BooleanField(default=0,
                                       help_text='If not set, the cooperative member will not receive SMS\'s when sent.')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'farmer_group'

    def __unicode__(self):
        return "{} ({})".format(self.name, self.village)

    def __str__(self):
        return "{} ({})".format(self.name, self.village)


class CertificationScope(TimeStampMixin):
    class CertificationScopeOption(models.TextChoices):
        EC = "EC" "EC"
        NOP = "NOP" "NOP"
        COR = "COR" "COR"
        KOFA = "KOFA" "KOFA"
        JAS = "JAS" "JAS"
        RFA = "RFA" "RFA"
        Other = "Other" "Other"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Farmer(TimeStampMixin):

    title = (
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
        ('Hon', 'Hon'),
    )
    months_choices = []
    for i in range(1, 13):
        months_choices.append((i, calendar.month_name[i]))

    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.SET_NULL)
    farmer_group = models.ForeignKey(FarmerGroup, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='member/', null=True, blank=True)
    member_id = models.CharField(max_length=150, unique=True, null=True, blank=True)
    title = models.CharField(max_length=25, choices=title, null=True, blank=True)
    surname = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    other_name = models.CharField(max_length=150, null=True, blank=True)
    is_refugee = models.BooleanField(default=False)
    is_handicap = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), null=True, blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True,
                                      choices=(('Single', 'Single'), ('Married', 'Married'),
                                                ('Widowed', 'Widow'), ('Divorced', 'Divorced')))
    id_number = models.CharField(max_length=150, null=True, blank=True, unique=True)
    id_type = models.CharField(max_length=150, null=True, blank=True,
                               choices=(('nin', 'National ID'), ('dl', 'Drivers Lisence'),
                                        ('pp', 'PassPort'), ('o', 'Other')))
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    other_phone_number = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.CASCADE)
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.CASCADE)
    parish = models.ForeignKey(Parish, null=True, blank=True, on_delete=models.CASCADE)
    village = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    gps_coordinates = models.CharField(max_length=150, null=True, blank=True)
    altitude = models.CharField(max_length=150, null=True, blank=True)
    certification_scopes = models.ManyToManyField(CertificationScope, blank=True)

    productive_coffee_trees = models.PositiveIntegerField(null=True, blank=True)
    non_productive_coffee_trees = models.PositiveIntegerField(null=True, blank=True)
    current_yield_estimate = models.PositiveIntegerField(null=True, blank=True)
    last_year_parch_harvest = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    last_year_cherry_harvest = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    coffee_acreage = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    other_crop_acreage = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    current_year_estimated_yield = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    conservation_acreage = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True, help_text='Area under conservation')
    total_acreage = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    organic_plots = models.PositiveIntegerField(null=True, blank=True)
    organic_plot_crop = models.ManyToManyField(Crop, related_name="farmer_organic_plot_crop")
    conventional_plots = models.PositiveIntegerField(null=True, blank=True)
    conventional_plot_crop = models.ManyToManyField(Crop, related_name="farmer_conventional_plot_crop")

    is_active = models.BooleanField(default=1)
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)
    app_id = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)


    class Meta:
        db_table = 'cooperative_member'

    def __str__(self):
        return "{} {} {}".format(self.surname, self.first_name or '', self.other_name or '')

    def get_name(self):
        return "%s %s %s" % (self.surname, self.first_name, self.other_name)

    def get_absolute_url(self):
        return reverse('events.views.details', args=[str(self.id)])

    @property
    def age(self):
        if self.date_of_birth:
            m = date.today() - self.date_of_birth
            return m.days / 365
        return None


class LandParcel(TimeStampMixin):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    size_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    boundary = models.PolygonField(geography=True, srid=4326)
    map_image = models.ImageField(upload_to=land_upload_path, blank=True, null=True)

    class Meta:
        db_table = 'land_parcel'


class FarmerInspection(TimeStampMixin):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    coffee_plots_change = models.BooleanField(help_text='Are coffee plots same as previously visited and as registered in Farm Entrance Form and Farm map?')
    comment = models.TextField(null=True, blank=True)
    previous_organic_plots = models.PositiveIntegerField(null=True, blank=True)
    organic_plots_added = models.PositiveIntegerField(null=True, blank=True)
    organic_plots_removed = models.PositiveIntegerField(null=True, blank=True)
    current_organic_plots = models.PositiveIntegerField(null=True, blank=True)
    conventional_plots = models.PositiveIntegerField(null=True, blank=True)
    organic_plot_crop = models.ManyToManyField(Crop, related_name="organic_plot_crop")
    conventional_plot_crop = models.ManyToManyField(Crop, related_name="conventional_plot_crop")

    class Meta:
        db_table = "farmer_inspection"
        verbose_name_plural = "Inspection"


class InspectionAttendee(TimeStampMixin):

    class FamilyRole(models.TextChoices):
        WIFE = "WIFE" "WIFE"
        SON = "SON" "SON"
        DAUGHTER = "DAUGHTER" "DAUGHTER"
        HUSBAND = "HUSBAND", "Husband"
        OTHER = "OTHER", "Other"

    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=FamilyRole.choices)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=120, null=True, blank=True)


    def __str__(self):
        return f"{self.name} ({self.role})"

    class Meta:
        db_table = "inspection_attendee"


class InspectionSeedAndPlantingStock(TimeStampMixin):
    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE)
    coffee_variety = models.CharField(max_length=255, help_text="Name of the coffee variety planted.")
    year_planted = models.PositiveIntegerField(help_text="Year the coffee was planted.")
    quantity = models.DecimalField(max_digits=9, decimal_places=2, help_text="Quantity of coffee plants or seeds.")
    supplier = models.CharField(max_length=255, null=True, blank=True, help_text="Supplier of the seeds/planting stock.")
    organic = models.PositiveIntegerField(null=True, blank=True, help_text="Quantity of organic plants/seeds.")
    treated = models.PositiveIntegerField(null=True, blank=True, help_text="Quantity of treated plants/seeds.")
    chemcal_used = models.TextField(null=True, blank=True, help_text="List of chemicals used on the plants/seeds.")
    gmo = models.CharField(max_length=120, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "inspection_seed_and_planting_stock"


class PlantProductionManagement(TimeStampMixin):
    """
    Section 5: Plant Production Management and Record Keeping
    """
    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='plant_production')

    is_contracted = models.BooleanField(null=True, blank=True,
                                        help_text="Farmer is contracted and contract form available")
    contract_comment = models.TextField(null=True, blank=True)

    keeps_farm_records = models.BooleanField(null=True, blank=True, help_text="Farmer keeps farm production records")
    farm_record_comment = models.TextField(null=True, blank=True)

    is_not_coffee_trader = models.BooleanField(null=True, blank=True, help_text="Farmer is not a coffee trader")
    coffee_trader_comment = models.TextField(null=True, blank=True)

    buffer_zone_present = models.BooleanField(null=True, blank=True,
                                              help_text="Buffer zone between coffee field and chemical field")
    buffer_zone_type = models.CharField(max_length=255, null=True, blank=True)
    buffer_zone_distance = models.CharField(max_length=255, null=True, blank=True)
    buffer_zone_comment = models.TextField(null=True, blank=True)

    attestation_new_plots = models.BooleanField(null=True, blank=True)
    attestation_new_plots_comment = models.TextField(null=True, blank=True)

    sketch_drawn = models.BooleanField(null=True, blank=True, help_text="Sketch of all plots drawn")
    sketch_drawn_comment = models.TextField(null=True, blank=True)

    trained_on_org_standards = models.BooleanField(null=True, blank=True)
    number_of_trainings = models.PositiveIntegerField(null=True, blank=True)
    last_training_date = models.DateField(null=True, blank=True)

    farm_clean = models.BooleanField(null=True, blank=True)
    farm_clean_comment = models.TextField(null=True, blank=True)

    neighbors_water_buffer = models.BooleanField(null=True, blank=True)
    neighbors_water_buffer_comment = models.TextField(null=True, blank=True)

    no_parallel_production = models.BooleanField(null=True, blank=True)
    no_parallel_production_comment = models.TextField(null=True, blank=True)

    sufficient_shade_trees = models.BooleanField(null=True, blank=True)
    sufficient_shade_trees_comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "plant_production_management"


    def __str__(self):
        return f"Plant Production Management - Inspection {self.inspection.pk}"


class SoilFertilityManagement(TimeStampMixin):
    """
    Section 6: Soil and Fertility Management
    """
    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='soil_fertility')

    soil_erosion_control = models.BooleanField(null=True, blank=True)
    soil_erosion_control_comments = models.TextField(null=True, blank=True)

    soil_fertility_measures = models.BooleanField(null=True, blank=True)
    soil_fertility_measures_comments = models.TextField(null=True, blank=True)

    no_disallowed_products = models.BooleanField(null=True, blank=True)
    no_disallowed_products_comments = models.TextField(null=True, blank=True)

    knowledge_on_manure = models.BooleanField(null=True, blank=True)
    manure_quantity_per_tree = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    manure_turning_times = models.PositiveIntegerField(null=True, blank=True)
    manure_interval = models.PositiveIntegerField(null=True, blank=True, help_text="Interval between turning (days)")
    manure_duration = models.CharField(max_length=255, null=True, blank=True)
    manure_month_of_application = models.CharField(max_length=50, null=True, blank=True)

    manure_compliant_cow_dung = models.PositiveIntegerField(null=True, blank=True)
    manure_compliant_goat_droppings = models.PositiveIntegerField(null=True, blank=True)
    manure_compliant_chicken_droppings = models.PositiveIntegerField(null=True, blank=True)
    manure_compliant_pig_dung = models.PositiveIntegerField(null=True, blank=True)
    manure_compliant_other = models.CharField(max_length=255, null=True, blank=True)

    does_not_apply_fresh_manure = models.BooleanField(null=True, blank=True)
    does_not_apply_fresh_manure_comments = models.TextField(null=True, blank=True)

    fresh_manure_no_flow_to_coffee = models.BooleanField(null=True, blank=True)
    fresh_manure_no_flow_to_coffee_comments = models.TextField(null=True, blank=True)

    does_not_use_treated_seed_as_intercrop = models.BooleanField(null=True, blank=True)
    intercrops_nitrogen_fixing = models.CharField(max_length=255, null=True, blank=True,
                                                  help_text="Crop intercrops nitrogen fixing")

    class Meta:
        db_table = "soil_fertility_management"

    def __str__(self):
        return f"Soil Fertility Management - Inspection {self.inspection.pk}"


class PestsAndDiseasesControl(TimeStampMixin):
    CRITERION_CHOICES = [
        ('C', 'Compliant'),
        ('NC', 'Non-Compliant'),
        ('NA', 'Not Applicable'),
    ]

    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='pests_and_diseases')
    # 7.1 Cases of pest and disease infestation
    cases_of_infestation = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    degree_of_infestation = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('Severe', 'Severe')],
        blank=True, null=True
    )

    # 7.2 Efforts to control pests and diseases
    efforts_to_control = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    # 7.3 No use of disallowed pesticides/fungicides
    disallowed_pesticides = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    material_used = models.CharField(max_length=200, blank=True, null=True)

    # 7.4 Other pest and disease control methods
    other_methods = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    method_description = models.TextField(blank=True, null=True)

    # 7.5 Efforts to minimize killing pollinators
    minimize_pollinators = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    # 7.6 Farmer does not use GMOs
    no_gmos = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Pests & Disease Control Record #{self.id}"

    class Meta:
        db_table = "pest_and_disease_control"


class WeedManagement(TimeStampMixin):
    CRITERION_CHOICES = [
        ('C', 'Compliant'),
        ('NC', 'Non-Compliant'),
        ('NA', 'Not Applicable'),
    ]

    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='weed_management')
    # 8.1 No use of Herbicides
    no_herbicides = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    # 8.2 Minimum weeding/slashing
    minimum_weeding = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    minimum_weeding_months = models.CharField(max_length=100, blank=True, null=True)

    # 8.3 Open weeding
    open_weeding = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    open_weeding_months = models.CharField(max_length=100, blank=True, null=True)

    # 8.4 No burning to control weeds
    no_burning = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    # Last year of chemical usage
    last_chemical_year = models.IntegerField(blank=True, null=True)
    chemicals_used = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Weed Management Record #{self.id}"

    class Meta:
        db_table = "weed_management"


class HarvestAndPostharvest(TimeStampMixin):
    CRITERION_CHOICES = [
        ('C', 'Compliant'),
        ('NC', 'Non-Compliant'),
        ('NA', 'Not Applicable'),
    ]

    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='harvest_post_harvest')
    picks_ripe_cherries = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    clean_containers = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    registered_pulper = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    proper_disposal_of_cherry_skins = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    clean_fermentation_materials = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    no_wastewater_discharge = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    clean_drying_facilities = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    organic_stored_separately = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)
    clean_coffee_store = models.CharField(max_length=2, choices=CRITERION_CHOICES, blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Harvest & Postharvest Record #{self.id}"

    class Meta:
        db_table = "harvest_and_postharvest"


class RiskOfContamination(TimeStampMixin):
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='rist_of_contamination')
    # 10.1 Use of unapproved inputs on organic farm
    unapproved_inputs = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, blank=True, null=True)
    unapproved_inputs_comment = models.TextField(blank=True, null=True)

    # 10.2 Neighbor using chemicals
    neighbor_using_chemicals = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, blank=True, null=True)
    neighbor_using_chemicals_comment = models.TextField(blank=True, null=True)

    # 10.3 Storage of unapproved materials in organic stores
    unapproved_storage = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, blank=True, null=True)
    unapproved_storage_comment = models.TextField(blank=True, null=True)

    # 10.4 Other specify
    other_risk = models.CharField(max_length=255, blank=True, null=True)
    other_risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, blank=True, null=True)
    other_risk_comment = models.TextField(blank=True, null=True)

    # Measure taken to minimize risk
    measures_taken = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "risk_of_contamination"

    def __str__(self):
        return f"Risk of Contamination Record #{self.id}"


class VisitedField(TimeStampMixin):
    inspection = models.ForeignKey(
        "FarmerInspection",
        on_delete=models.CASCADE,
        related_name="visited_fields"
    )
    inspection = models.ForeignKey(FarmerInspection, on_delete=models.CASCADE, related_name='visited_field')
    sn = models.PositiveIntegerField(help_text="Serial number", null=True, blank=True)
    name_of_field = models.CharField(max_length=255, help_text="Name of the field or plot")

    young_coffee = models.PositiveIntegerField(null=True, blank=True, help_text="Number of young coffee trees")
    stumped_coffee = models.PositiveIntegerField(null=True, blank=True, help_text="Number of stumped coffee trees")
    productive_coffee = models.PositiveIntegerField(null=True, blank=True, help_text="Number of productive coffee trees")
    ye_coffee = models.PositiveIntegerField(null=True, blank=True, help_text="Number of yet-to-enter (YE) coffee trees")

    area = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, help_text="Field area (e.g., acres or hectares)")
    comments = models.TextField(null=True, blank=True, help_text="Comments or observations during inspection")

    def __str__(self):
        return f"Visited Field Record #{self.id}"

    class Meta:
        db_table = "visited_field"


class Collection(TimeStampMixin):
    collection_date = models.DateTimeField()
    is_member = models.BooleanField(default=1)
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey(Farmer, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    collection_reference = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = 'collection'


class FarmerTransaction(TimeStampMixin):

    TRANSACTION_TYPES = [
        ('ORDER_DEBIT', 'Order Debit'),  # Farmer buys goods
        ('PRODUCE_CREDIT', 'Produce Credit'),  # Farmer brings produce
        ('CASH_CREDIT', 'Cash Credit Given'),  # Farmer receives money
        ('PAYMENT', 'Payment Made by Farmer'), # Farmer pays back
        ('ADJUSTMENT', 'Adjustment'),
    ]

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('NONE', 'None'),
    ]

    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='NONE')

    # Positive = credit (farm owes farmer)
    # Negative = debit (farmer owes farm)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    reference = models.CharField(max_length=255, blank=True, null=True)  # order_no, produce_no, etc.
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer} - {self.transaction_type} - {self.amount}"