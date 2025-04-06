from django.db import models
#from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator
from django.utils import timezone

class LandParcel(models.Model):
    """Model representing a land parcel available for leasing"""
    
    # Basic parcel information
    parcel_id = models.CharField(max_length=50, unique=True, verbose_name="Parcel ID")
    title = models.CharField(max_length=200, verbose_name="Parcel Title")
    description = models.TextField(verbose_name="Description")
    
    # Location information
    #location = gis_models.PointField(verbose_name="Geographic Location")
    address = models.TextField(verbose_name="Physical Address")
    region = models.CharField(max_length=100, verbose_name="Region/State")
    city = models.CharField(max_length=100, verbose_name="City/Town")
    sub_City = models.CharField(max_length=100, verbose_name="Sub-City")
    woreda = models.CharField(max_length=100, verbose_name="Woreda")
    kebele = models.CharField(max_length=100, verbose_name="Kebele")
    street = models.CharField(max_length=100, verbose_name="Street")
    house_number = models.CharField(max_length=100, verbose_name="House Number")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal Code")
  
  
    
    # Size information
    area = models.DecimalField(max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Area (square meters)"
    )
    
    # Zoning and classification
    ZONING_CHOICES = [
        ('RES', 'Residential'),
        ('COM', 'Commercial'),
        ('IND', 'Industrial'),
        ('AGR', 'Agricultural'),
        ('MIX', 'Mixed Use'),
        ('OTH', 'Other'),
    ]
    zoning_type = models.CharField(
        max_length=3,
        choices=ZONING_CHOICES,
        verbose_name="Zoning Type"
    )
    
    # Ownership information
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='owned_parcels',
        verbose_name="Owner"
    )
    owner_name = models.CharField(max_length=100, verbose_name="Owner Name")
    owner_id = models.CharField(max_length=50, unique=True, verbose_name="Owner ID")
    owner_email = models.EmailField(max_length=100, verbose_name="Owner Email")
    owner_address = models.TextField(verbose_name="Owner Address")
    owner_phone = models.CharField(max_length=20, verbose_name="Owner Phone")
    owner_national_id = models.CharField(max_length=50, verbose_name="Owner National ID")
    owner_type = models.CharField(
            max_length=50,
            choices=[
                ('INDIVIDUAL', 'Individual'),
                ('CORPORATE', 'Corporate'),
                ('GOVERNMENT', 'Government'),
                ('NGO', 'Non-Governmental Organization'),
            ],
            verbose_name="Owner Type"

    )
    is_public_land = models.BooleanField(default=False, verbose_name="Public Land")
    
    # Status information
    STATUS_CHOICES = [
        ('AVAIL', 'Available'),
        ('LEASED', 'Leased'),
        ('PEND', 'Pending Approval'),
        ('UNAVAIL', 'Unavailable'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default='AVAIL',
        verbose_name="Status"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Documents and attachments would be handled via a separate model
    
    class Meta:
        verbose_name = "Land Parcel"
        verbose_name_plural = "Land Parcels"
        ordering = ['parcel_id']
    
    def __str__(self):
        return f"{self.parcel_id} - {self.title}"


class LeaseOffer(models.Model):
    """Model representing a leasing offer for a land parcel"""
    
    parcel = models.ForeignKey(
        LandParcel,
        on_delete=models.CASCADE,
        related_name='lease_offers',
        verbose_name="Land Parcel"
    )
    
    # Lease terms
    lease_type = models.CharField(
        max_length=50,
        choices=[
            ('SHORT', 'Short-term (1-5 years)'),
            ('MED', 'Medium-term (5-15 years)'),
            ('LONG', 'Long-term (15+ years)'),
            ('PERP', 'Perpetual'),
        ],
        verbose_name="Lease Type"
    )
    duration_months = models.PositiveIntegerField(verbose_name="Lease Duration (months)")
    
    # Pricing information
    price_per_month = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Monthly Price"
    )
    security_deposit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Security Deposit"
    )
    payment_terms = models.TextField(verbose_name="Payment Terms")
    
    # Offer details
    offer_start_date = models.DateField(verbose_name="Offer Start Date")
    offer_end_date = models.DateField(verbose_name="Offer End Date")
    is_public = models.BooleanField(default=True, verbose_name="Public Offer")
    
    # Restrictions and conditions
    allowed_uses = models.TextField(verbose_name="Allowed Uses")
    restrictions = models.TextField(verbose_name="Usage Restrictions", blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('WITHDRAWN', 'Withdrawn'),
        ('ACCEPTED', 'Accepted'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Status"
    )
    
    # Metadata
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='created_offers',
        verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Lease Offer"
        verbose_name_plural = "Lease Offers"
        ordering = ['-offer_start_date']
    
    def __str__(self):
        return f"Lease Offer for {self.parcel.parcel_id} ({self.get_status_display()})"
    
    @property
    def is_active(self):
        """Check if the offer is currently active"""
        today = timezone.now().date()
        return (self.status == 'ACTIVE' and 
                self.offer_start_date <= today <= self.offer_end_date)


class LeaseApplication(models.Model):
    """Model representing applications for land lease offers"""
    
    offer = models.ForeignKey(
        LeaseOffer,
        on_delete=models.PROTECT,
        related_name='applications',
        verbose_name="Lease Offer"
    )
    applicant = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='lease_applications',
        verbose_name="Applicant"
    )
    
    # Application details
    proposed_use = models.TextField(verbose_name="Proposed Use")
    business_plan = models.TextField(verbose_name="Business Plan", blank=True)
    supporting_docs = models.TextField(verbose_name="Supporting Documents", blank=True)
    
    # Status of the application
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='SUBMITTED',
        verbose_name="Status"
    )
    
    # Review information
    review_notes = models.TextField(verbose_name="Review Notes", blank=True)
    reviewed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        verbose_name="Reviewed By"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Review Date")
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Lease Application"
        verbose_name_plural = "Lease Applications"
        ordering = ['-submitted_at']
        unique_together = ['offer', 'applicant']
    
    def __str__(self):
        return f"Application by {self.applicant} for {self.offer}"


class DocumentAttachment(models.Model):
    """Model for storing documents related to parcels, offers, or applications"""
    
    DOCUMENT_TYPES = [
        ('TITLE', 'Title Deed'),
        ('SURVEY', 'Survey Document'),
        ('ZONING', 'Zoning Certificate'),
        ('PLAN', 'Site Plan'),
        ('OTHER', 'Other'),
    ]
    
    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPES,
        verbose_name="Document Type"
    )
    file = models.FileField(upload_to='land_leases/documents/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    
    # Generic foreign key approach to link to different models
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    #content_object = models.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = "Document Attachment"
        verbose_name_plural = "Document Attachments"
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.description or 'No description'}"
    

  