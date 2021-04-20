from bottle import Bottle

from rest.backstage import BackStage
from rest.revenue import Revenue
from rest.bidder import Bidder
from rest.broker import Broker
from rest.tasks import Tasks
from rest.websites.website import Websites
from rest.websites.medium import Mediums
from rest.websites.keyword import Keywords
from rest.websites.device import Devices
from rest.websites.inpage import Inpage
from rest.websites.campaigns import Campaigns
from rest.websites.countries import Countries
from rest.dealer import Dealer
from rest.optimization import Optimization
from rest.realtime.campaigns import RTCampaigns
from rest.validation import Validation
from rest.factor import Factor
from rest.report_dynamic import ReportDynamic
from rest.auto_managment import AutomationManagment
from rest.hourly_roi import HourlyRoi

from rest.campaign_manager.campaigns import cmCampaigns
from rest.campaign_manager.properties import cmProperties
from rest.campaign_manager.inventory import cmInventory
from rest.campaign_manager.targeting import cmTargeting
from rest.campaign_manager.widget_optimization import cmWidgetOpt
from rest.campaign_manager.profiler import Profiler


restApp = application = Bottle()

restApp.merge(BackStage)
restApp.merge(Revenue)
restApp.merge(Tasks)
restApp.merge(Websites)
restApp.merge(Mediums)
restApp.merge(Keywords)
restApp.merge(Devices)
restApp.merge(Inpage)
restApp.merge(Campaigns)
restApp.merge(Countries)
restApp.merge(Dealer)
restApp.merge(Bidder)
restApp.merge(Broker)
restApp.merge(RTCampaigns)

restApp.merge(cmCampaigns)
restApp.merge(cmProperties)
restApp.merge(cmInventory)
restApp.merge(cmTargeting)
restApp.merge(cmWidgetOpt)
restApp.merge(Profiler)
restApp.merge(Optimization)
restApp.merge(Validation)
restApp.merge(Factor)
restApp.merge(ReportDynamic)
restApp.merge(AutomationManagment)
restApp.merge(HourlyRoi)



#---------------------------------------------------------------------------#
# Exported symbols
#---------------------------------------------------------------------------#
__all__ = [
    "restApp"
]