from django.contrib import admin
from .models import *
from .models import ContactMessage, FAQ
from .models import OfferBanner, BogoProduct, ExclusiveOffer, NewsletterSection
from .models import AboutPage, CoreValue, FounderSection, CommitmentSection
from .models import LoginRecord
admin.site.register(Banner)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(WhyGlowify)
admin.site.register(Testimonial)
admin.site.register(SiteSetting)
admin.site.register(NavLink)
admin.site.register(LoginRecord)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'mobile')

    readonly_fields = ('full_name', 'email', 'mobile', 'message', 'created_at')

    def has_add_permission(self, request):
        return False  # admin manually add panna vendam


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)



@admin.register(OfferBanner)
class OfferBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    
@admin.register(BogoProduct)
class BogoProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sale_price', 'order']
    list_editable = ['order']

@admin.register(ExclusiveOffer)
class ExclusiveOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    list_display = ['heading', 'is_active']



@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {'fields': ('hero_title', 'hero_subtitle', 'hero_bg_image')}),
        ('Our Story', {'fields': ('story_title', 'story_content', 'story_image')}),
        ('Our Mission', {'fields': ('mission_title', 'mission_content')}),
        ('Status', {'fields': ('is_active',)}),
    )

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']

@admin.register(FounderSection)
class FounderSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'founder_name', 'is_active']

@admin.register(CommitmentSection)
class CommitmentSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']