from django.db import models


class Currency(models.Model):
	date = models.DateField('date')
	BYR = models.FloatField('BYR')
	USD = models.FloatField('USD')
	EUR = models.FloatField('EUR')
	KZT = models.FloatField('KZT')
	UAH = models.FloatField('UAH')
	AZN = models.FloatField('AZN')
	KGS = models.FloatField('KGS')
	UZS = models.FloatField('UZS')
	GEL = models.FloatField('GEL')
