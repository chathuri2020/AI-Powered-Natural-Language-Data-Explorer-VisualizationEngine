# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=50)
    district = models.ForeignKey('District', models.DO_NOTHING)
    frequency = models.CharField(max_length=26)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'account'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Card(models.Model):
    card_id = models.CharField(primary_key=True, max_length=50)
    disp = models.ForeignKey('Disposition', models.DO_NOTHING)
    type = models.CharField(max_length=14)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'card'


class Client(models.Model):
    client_id = models.CharField(primary_key=True, max_length=50)
    sex = models.CharField(max_length=50)
    fulldate = models.DateField()
    age = models.IntegerField()
    social = models.CharField(max_length=50)
    first = models.CharField(max_length=50)
    middle = models.CharField(max_length=50, blank=True, null=True)
    last = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    district = models.ForeignKey('District', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'client'


class Clientaccount(models.Model):
    client_id = models.CharField(primary_key=True, max_length=10)
    account_id = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientaccount'


class Crmcallcenterlogs(models.Model):
    date_received = models.CharField(db_column='Date received', max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    complaint_id = models.CharField(db_column='Complaint ID', max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rand_client = models.CharField(db_column='rand client', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    phonefinal = models.CharField(max_length=50, blank=True, null=True)
    vru_line = models.CharField(db_column='vru+line', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    call_id = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    outcome = models.CharField(max_length=50, blank=True, null=True)
    server = models.CharField(max_length=50, blank=True, null=True)
    ser_start = models.CharField(max_length=50)
    ser_exit = models.CharField(max_length=50)
    ser_time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'crmcallcenterlogs'


class Crmevents(models.Model):
    date_received = models.DateField(db_column='Date received')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    product = models.CharField(db_column='Product', max_length=50)  # Field name made lowercase.
    sub_product = models.CharField(db_column='Sub-product', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    issue = models.CharField(db_column='Issue', max_length=50)  # Field name made lowercase.
    sub_issue = models.CharField(db_column='Sub-issue', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    consumer_complaint_narrative = models.TextField(db_column='Consumer complaint narrative', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tags = models.CharField(db_column='Tags', max_length=50, blank=True, null=True)  # Field name made lowercase.
    consumer_consent_provided_field = models.CharField(db_column='Consumer consent provided?', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    submitted_via = models.CharField(db_column='Submitted via', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_sent_to_company = models.CharField(db_column='Date sent to company', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    company_response_to_consumer = models.CharField(db_column='Company response to consumer', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    timely_response_field = models.CharField(db_column='Timely response?', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    consumer_disputed_field = models.CharField(db_column='Consumer disputed?', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    complaint_id = models.CharField(db_column='Complaint ID', primary_key=True, max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='Client_ID', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'crmevents'


class Crmreviews(models.Model):
    reviewid = models.AutoField(db_column='reviewId', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    stars = models.IntegerField(db_column='Stars')  # Field name made lowercase.
    reviews = models.CharField(db_column='Reviews', max_length=255, blank=True, null=True)  # Field name made lowercase.
    product = models.CharField(db_column='Product', max_length=50)  # Field name made lowercase.
    district = models.ForeignKey('District', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'crmreviews'


class Disposition(models.Model):
    disp_id = models.CharField(primary_key=True, max_length=10)
    client = models.ForeignKey(Clientaccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'disposition'


class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=50)
    state_name = models.ForeignKey('State', models.DO_NOTHING, db_column='state_name')

    class Meta:
        managed = False
        db_table = 'district'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Loan(models.Model):
    loan_id = models.CharField(max_length=50)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    amount = models.IntegerField()
    duration = models.IntegerField()
    payments = models.IntegerField()
    status = models.CharField(max_length=50)
    date = models.DateField()
    location = models.IntegerField()
    purpose = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'loan'


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    bank_to = models.CharField(max_length=50)
    account_to = models.IntegerField()
    amount = models.IntegerField()
    k_symbol = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class State(models.Model):
    state_name = models.CharField(primary_key=True, max_length=50)
    state_abbrev = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    division = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'state'


class Transaction(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=50)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    type = models.CharField(max_length=50)
    operation = models.CharField(max_length=50, blank=True, null=True)
    amount = models.IntegerField()
    balance = models.IntegerField()
    k_symbol = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    account_0 = models.CharField(db_column='account', max_length=50, blank=True, null=True)  # Field renamed because of name conflict.
    date = models.CharField(max_length=50, blank=True, null=True)
    fulldatewithtime = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'
