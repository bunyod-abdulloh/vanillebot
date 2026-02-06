from loader import dp
from .admins import IsBotAdminFilter
from .users import IsUserJoined, IsUserLeft

if __name__ == "filters":
    dp.filters_factory.bind(IsBotAdminFilter)
    dp.filters_factory.bind(IsUserJoined)
    dp.filters_factory.bind(IsUserLeft)
