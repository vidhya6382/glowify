from django.db import models

# ===================== SITE SETTINGS =====================
class SiteSetting(models.Model):
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    address = models.TextField(default="3rd Floor, Valasaravakkam, Chennai - 600800")

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name_plural = "Site Settings"


# ===================== NAV LINKS =====================
class NavLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200, default="#")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ===================== BANNER =====================
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    title = models.CharField(max_length=200, blank=True, default="")
    subtitle = models.CharField(max_length=200, blank=True, default="")
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_url = models.CharField(max_length=200, default="#")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or "Banner"


# ===================== INGREDIENTS =====================
class Ingredient(models.Model):
    image = models.ImageField(upload_to='ingredients/')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ===================== PRODUCT (ONLY ONE MODEL) =====================
class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    reviews_count = models.IntegerField(default=0)
    tag = models.CharField(max_length=50, blank=True, default="")
    is_featured = models.BooleanField(default=True)

    brand = models.CharField(max_length=100, default='Lakme')
    color = models.CharField(max_length=50, default='Pink')

    def __str__(self):
        return self.name


# ===================== CATEGORY =====================
class Category(models.Model):
    image = models.ImageField(upload_to='categories/')
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, default="")
    button_url = models.CharField(max_length=200, default="#")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# ===================== WHY GLOWIFY =====================
class WhyGlowify(models.Model):
    image = models.ImageField(upload_to='why/', blank=True, null=True)
    point = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Why Glowify Points"

    def __str__(self):
        return self.point


# ===================== TESTIMONIAL =====================
class Testimonial(models.Model):
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review = models.TextField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, default="")
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.name


# ===================== CONTACT =====================
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


# ===================== FAQ =====================
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


# ===================== OFFERS =====================
class OfferBanner(models.Model):
    title = models.CharField(max_length=200, default="BIG SALE!")
    subtitle = models.CharField(max_length=200, default="UP TO 50% OFF")
    offer_text = models.CharField(max_length=200, default="LIMITED TIME OFFER")
    heading = models.CharField(max_length=200, default="Unbeatable Deals on Top Brands!")
    sub_heading = models.CharField(max_length=300, default="Shop now and save big")
    banner_image = models.ImageField(upload_to='offers/banners/')
    discount_1 = models.CharField(max_length=10, default="40%")
    discount_2 = models.CharField(max_length=10, default="30%")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Main Offer Banner"
        verbose_name_plural = "Main Offer Banner"


class BogoProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='offers/products/')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Buy 1 Get 1 Product"
        verbose_name_plural = "Buy 1 Get 1 Products"


class ExclusiveOffer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='offers/exclusive/')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=35)
    button_text = models.CharField(max_length=50, default="Claim This Offer")
    is_active = models.BooleanField(default=True)


class NewsletterSection(models.Model):
    heading = models.CharField(max_length=200, default="Join The Inner Circle")
    description = models.CharField(max_length=300, default="Exclusive offers and tips")
    button_text = models.CharField(max_length=50, default="Register")
    background_image = models.ImageField(upload_to='offers/newsletter/', blank=True, null=True)
    is_active = models.BooleanField(default=True)


# ===================== ABOUT PAGE =====================
class AboutPage(models.Model):
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    hero_bg_image = models.ImageField(upload_to='about/hero/')

    story_title = models.CharField(max_length=200)
    story_content = models.TextField()
    story_image = models.ImageField(upload_to='about/story/')

    mission_title = models.CharField(max_length=200)
    mission_content = models.TextField()

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"


class CoreValue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='about/values/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class FounderSection(models.Model):
    title = models.CharField(max_length=200)
    founder_name = models.CharField(max_length=100)
    founder_image = models.ImageField(upload_to='about/founder/')
    content = models.TextField()
    is_active = models.BooleanField(default=True)


class CommitmentSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    button_text = models.CharField(max_length=100)
    button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


# ===================== LOGIN RECORD (NOT SECURE FOR PRODUCTION) =====================
class LoginRecord(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    tagline = models.CharField(max_length=200, default="Luxury. Comfort. Timeless Color.")
    net_weight = models.CharField(max_length=50, default="3.5g")
    finish = models.CharField(max_length=100, default="Cream Luxe (Satin Glow)")
    skin_type = models.CharField(max_length=100, default="Suitable for all")
    is_featured = models.BooleanField(default=False) # ADD THIS LINE
    
    def __str__(self):
        return self.name