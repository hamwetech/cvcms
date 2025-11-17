from django.contrib import admin
from django.contrib.admin import ModelAdmin
# from unfold.admin import ModelAdmin
# from django.contrib import ModelAdmin
from conf.models import District, County, SubCounty, Parish, Village, PaymentMethod, SystemSettings, Region, Crop, \
    Product, ProductVariation, ProductVariationPrice, ProductUnit


# admin.site.unregister(District)
# admin.site.unregister(County)

@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('region', 'name',)


@admin.register(County)
class CountyAdmin(ModelAdmin):
    list_display = ('district', 'name',)


@admin.register(SubCounty)
class SubCountyAdmin(ModelAdmin):
    list_display = ('county', 'name',)


@admin.register(Parish)
class ParishAdmin(ModelAdmin):
    list_display = ('sub_county', 'name',)


@admin.register(Crop)
class CropAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(ProductUnit)
class ProductUnitAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(ProductVariation)
class ProductVariationAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(ProductVariationPrice)
class ProductVariationPriceAdmin(ModelAdmin):
    list_display = ('product', 'price')