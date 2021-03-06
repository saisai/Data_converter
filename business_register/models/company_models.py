from django.db import models
from simple_history.models import HistoricalRecords
from business_register.models.kved_models import Kved
from data_ocean.models import Authority, DataOceanModel, Status, TaxpayerType


class Bylaw(DataOceanModel):
    name = models.CharField(max_length=320, unique=True, null=True)


class CompanyType(DataOceanModel):
    name = models.CharField(max_length=270, unique=True, null=True)


class Company(DataOceanModel):  # constraint for not null in both name & short_name fields
    INVALID = 'invalid'  # constant for empty edrpou fild etc.
    name = models.CharField(max_length=500, null=True)
    short_name = models.CharField(max_length=500, null=True)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE)
    edrpou = models.CharField(max_length=260, db_index=True)
    address = models.CharField(max_length=1000, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    bylaw = models.ForeignKey(Bylaw, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(null=True)
    registration_info = models.CharField(max_length=450, null=True)
    contact_info = models.CharField(max_length=310, null=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    hash_code = models.CharField(max_length=510)
    history = HistoricalRecords()


class Assignee(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='assignees')
    name = models.CharField(max_length=610, null=True)
    hash_code = models.CharField(max_length=510)


class BancruptcyReadjustment(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bancruptcy_readjustment')
    op_date = models.DateTimeField(null=True)
    reason = models.TextField(null=True)
    sbj_state = models.CharField(max_length=345, null=True)
    head_name = models.CharField(max_length=515, null=True)
    hash_code = models.CharField(max_length=510)


class CompanyDetail(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_detail')
    founding_document_number = models.CharField(max_length=375, null=True)
    executive_power = models.CharField(max_length=390, null=True)
    superior_management = models.CharField(max_length=620, null=True)
    authorized_capital = models.CharField(max_length=560, null=True)
    managing_paper = models.CharField(max_length=360, null=True)
    terminated_info = models.CharField(max_length=600, null=True)
    termination_cancel_info = models.CharField(max_length=570, null=True)
    vp_dates = models.TextField(null=True)
    hash_code = models.CharField(max_length=510)
    history = HistoricalRecords()


class CompanyToKved(DataOceanModel):  # constraint for only only one truth in primary field
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='kveds')
    kved = models.ForeignKey(Kved, on_delete=models.CASCADE)
    primary_kved = models.BooleanField(default=False)
    hash_code = models.CharField(max_length=510)


class ExchangeDataCompany(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='exchange_data')
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    taxpayer_type = models.ForeignKey(TaxpayerType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    start_number = models.CharField(max_length=555, null=True)
    end_date = models.DateTimeField(null=True)
    end_number = models.CharField(max_length=555, null=True)
    hash_code = models.CharField(max_length=510)


class FounderFull(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='founders')
    name = models.TextField(null=True)
    edrpou = models.CharField(max_length=9, null=True)
    equity = models.FloatField(null=True)
    hash_code = models.CharField(max_length=510)
    history = HistoricalRecords()


class FounderNew(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='founders_new')
    name = models.TextField(null=True)
    edrpou = models.CharField(max_length=9, null=True)
    equity = models.FloatField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'company'], )
        ]


class Predecessor(DataOceanModel):  # constraint for not null in both fields
    name = models.CharField(max_length=500, null=True)
    code = models.CharField(max_length=405, null=True)


class CompanyToPredecessor(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='predecessors')
    predecessor = models.ForeignKey(Predecessor, on_delete=models.CASCADE)
    hash_code = models.CharField(max_length=510)


class Signer(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='signers')
    name = models.CharField(max_length=390, null=True)
    hash_code = models.CharField(max_length=510)
    history = HistoricalRecords()


class TerminationStarted(DataOceanModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='termination_started')
    op_date = models.DateTimeField(null=True)
    reason = models.TextField(null=True)
    sbj_state = models.CharField(max_length=530, null=True)
    signer_name = models.CharField(max_length=480, null=True)
    creditor_reg_end_date = models.DateTimeField(null=True)
    hash_code = models.CharField(max_length=510)
