import datetime
import csv
from webapp.models import (
	Store,
	Offer,
	ProductCategory,
)

STORE_OFFERS_DATA_FILES='offers/{storeName}/{catId}/{date}.csv'

class CuelinksOffersHandler():

	def __init__(self, *args, **kwargs):
		return super(CuelinksOffersHandler, self).__init__(*args, **kwargs)

	def read_offers_csv(self, catId):
		self.catId=catId
		date=datetime.datetime.now().date().strftime('%d-%m-%y')
		fileName=STORE_OFFERS_DATA_FILES.format(storeName='cuelinks', date=date, catId=catId)
		offers=[]
		with open(fileName, 'r') as f:
			reader=csv.reader(f, delimiter=',')
			for line in reader:
				offers.append(line)
			f.close()
		return offers[1:]

	def save_offers(self, offersList):
		offers=[]
		for offer in offersList:
			off, created=Offer.objects.get_or_create(
				offerId=int(offer[0]), 
				startTime=datetime.datetime.strptime(offer[9], '%Y-%m-%d'),
				endTime=datetime.datetime.strptime(offer[10], '%Y-%m-%d')
			)
			if created:
				off.title=offer[1]
				off.categories=offer[3]
				off.description=offer[4]
				off.terms=offer[5]
				off.coupoun_code=offer[6]
				off.url=offer[7]
				off.status=offer[8]
				off.imageUrl=offer[12]
				off.store, created=Store.objects.get_or_create(aff_name=offer[2])
				cat, new=ProductCategory.objects.get_or_create(catId=self.catId, name=self.catId)
				if new:
					off.store.categories.add(cat)
					off.store.save()
				off.category=cat
				off.save()
			else:
				# Update if the offer has been expired
				if off.endTime.ctime()<datetime.datetime.now().ctime():
					off.status='expired'
					off.save()
			offers.append(off)
		return offers