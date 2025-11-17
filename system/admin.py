from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# from unfold.admin import ModelAdmin
# from unfold.admin import StackedInline, TabularInline

from django.contrib.admin import ModelAdmin, StackedInline, TabularInline

from system.forms import PlantProductionManagementForm, SoilFertilityManagementForm
from system.models.models import (
    Farmer,
    FarmerInspection,
    CertificationScope,
    PlantProductionManagement,
    SoilFertilityManagement,
    InspectionAttendee,
    InspectionSeedAndPlantingStock,
    PestsAndDiseasesControl, WeedManagement, HarvestAndPostharvest, RiskOfContamination, VisitedField, Collection
)


@admin.register(CertificationScope)
class CertificationScopeAdmin(ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Farmer)
class FarmerAdmin(ModelAdmin):
    # form = FarmerForm
    fieldsets = (
        ('Personal Information', {
            'fields': ('image', 'title', 'first_name', 'other_name', 'surname', 'gender', 'date_of_birth', 'marital_status',
                       'is_refugee', 'is_handicap'), "classes": ("tab-basic",)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'other_phone_number', 'email', 'address', 'village', 'gps_coordinates',
                       'altitude'), "classes": ("tab-address",)
        }),
        ('Location Information', {
            'fields': ('district', 'county', 'sub_county', 'parish'), "classes": ("tab-location",)
        }),
        ('Coffee and Crop Information', {
            'fields': ('productive_coffee_trees', 'non_productive_coffee_trees', 'current_yield_estimate',
                       'last_year_parch_harvest', 'last_year_cherry_harvest', 'coffee_acreage', 'other_crop_acreage',
                       'current_year_estimated_yield', 'conservation_acreage', 'total_acreage'), "classes": ("tab-crop",)
        }),
        ('Organic and Conventional Plot Information', {
            'fields': ('organic_plots', 'organic_plot_crop', 'conventional_plots', 'conventional_plot_crop'), "classes": ("tab-plot",)
        }),
        ('Certification and Cooperative', {
            'fields': ('certification_scopes', 'cooperative', 'farmer_group'), "classes": ("tab-certification",)
        }),
        # ('Metadata', {
        #     'fields': ('create_by', 'create_date', 'update_date', 'is_active', 'qrcode', 'app_id')
        # }),
    )

    list_display = ( '_full_name', 'image','gender', 'date_of_birth', 'action_buttons')

    class Media:
        js = ("admin/js/tab_control_buttons.js",)

    def _full_name(self, obj):
        return f"{obj.title} {obj.surname} {obj.first_name}"

    def action_buttons(self, obj):
        view_url = reverse('admin:system_farmer_change', args=[obj.id])
        delete_url = reverse('admin:system_farmer_delete', args=[obj.id])

        return format_html(
            '<a class="btn btn-outline-warning" href="{}" style="margin-right:5px;"><i class="fa fa-edit"></i> Open</a>'
            '<a class="btn btn-outline-danger" href="{}" ><i class="fa fa-trash"></i> Delete</a>',
            view_url,
            delete_url,
        )

    action_buttons.short_description = "Actions"
    action_buttons.allow_tags = True
    _full_name.short_description = "Full Name"


# @admin.register(FarmerInspection)
# class FarmerInspectionAdmin(ModelAdmin):
#     list_display = ('farmer', 'inspection_date', 'coffee_plots_change')


class PlantProductionManagementInline(StackedInline):
    model = PlantProductionManagement
    form = PlantProductionManagementForm
    extra = 0
    ordering_field = 'farmer_inspection'

class SoilFertilityManagementInline(StackedInline):
    model = SoilFertilityManagement
    form = SoilFertilityManagementForm
    extra = 0
    ordering_field = 'farmer_inspection'

class InspectionAttendeeInline(StackedInline):
    model = InspectionAttendee
    extra = 1
    ordering_field = 'farmer_inspection'

class InspectionSeedAndPlantingStockInline(StackedInline):
    model = InspectionSeedAndPlantingStock
    extra = 1
    ordering_field = 'farmer_inspection'

class PestsAndDiseasesControlInline(StackedInline):
    model = PestsAndDiseasesControl
    extra = 1
    ordering_field = 'farmer_inspection'

class WeedManagementManagementInline(StackedInline):
    model = WeedManagement
    extra = 1
    ordering_field = 'farmer_inspection'

class HarvestAndPostharvestInline(StackedInline):
    model = HarvestAndPostharvest
    extra = 1
    ordering_field = 'farmer_inspection'

class RiskOfContaminationInline(StackedInline):
    model = RiskOfContamination
    extra = 1
    ordering_field = 'farmer_inspection'

class VisitedFieldInline(TabularInline):
    model = VisitedField
    extra = 1
    ordering_field = 'farmer_inspection'

@admin.register(FarmerInspection)
class FarmerInspectionAdmin(ModelAdmin):
    list_display = ('farmer', 'inspection_date', 'coffee_plots_change', 'created_at')
    search_fields = ('farmer__name', )
    list_filter = ('inspection_date', 'coffee_plots_change')

    inlines = [
        PlantProductionManagementInline,
        SoilFertilityManagementInline,
        InspectionAttendeeInline,
        InspectionSeedAndPlantingStockInline,
        PestsAndDiseasesControlInline,
        WeedManagementManagementInline,
        HarvestAndPostharvestInline,
        RiskOfContaminationInline,
        VisitedFieldInline,


    ]

    class Media:
        js = ("admin/js/tab_control_buttons.js",)


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = ('member', 'collection_reference', 'product', 'collection_date')
    search_fields = ('member__name', )
    list_filter = ('member', 'collection_date')


class CustomAdminSite(admin.AdminSite):
    site_header = "Customer Management Dashboard"
    site_title = "Customer Portal"
    index_title = "Welcome to the Customer Index"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.custom_index), name='index'),
        ]
        return custom_urls + urls

    def custom_index(self, request):
        app_list = self.get_app_list(request)  # 🧠 get the normal admin app list

        context = dict(
            self.each_context(request),
            title=_("Customer Dashboard"),
            app_list=app_list,  # 🧩 pass it to the template
            stats={
                "total_customers": 120,
                "active_customers": 85,
                "inactive_customers": 35,
            }
        )
        return render(request, "admin/index.html", context)

    # def custom_index(self, request):
    #     context = dict(
    #         self.each_context(request),
    #         title=_("Customer Overview"),
    #         stats={
    #             "total_customers": 120,
    #             "active_customers": 85,
    #             "inactive_customers": 35,
    #         }
    #     )
    #     return render(request, "admin/index.html", context)


custom_admin_site = CustomAdminSite(name='custom_admin')