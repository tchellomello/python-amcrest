from gpscrest.constants import HEADERS, COUNTRIES_URL, LAZY


class GPSCrestBase:

    def __init__(self):
        """Base class for GPSCrest."""
        self._info: dict = None
        self._parent: object = None
        self._countries: dict = None
        self._lazy: bool = LAZY

    def _inspect_attribute(self, attr) -> str:
        """
        Create generic return for attribute.

        It will basically scan the attributes to determine
        if the object must return from _parent or for top level.

        GPSCrest object will have _parent set to None
        GPSCrestDevice will have _parent set to GPScrest 
        itself to allow recursivity
        """
        if self._parent is None:
            try:
                return getattr(self._info, attr)
            except AttributeError:
                return getattr(self, attr)
        else:
            return getattr(self._parent, attr)

    @property
    def lazy(self) -> bool:
        return self._inspect_attribute('_lazy')

    @property
    def token(self):
        return self._inspect_attribute('token')

    @property
    def _headers(self):
        HEADERS['token'] = self.token
        return HEADERS

    @property
    def customer_id(self) -> str:
        return self._inspect_attribute('customer_id')

    @property
    def topic_id(self) -> str:
        return self._inspect_attribute('topic_id')

    @property
    def countries(self) -> str:
        return self._inspect_attribute('_countries')

    async def refresh(self):
        """Call method to refresh current location."""
        if self._parent:
            await self._parent.get_imei_info() 
        else:
            await self.get_imei_info() 

    async def get_country_list(self):
        """Populates country list."""
        self._countries = await self.Fetcher.post(url=COUNTRIES_URL, headers=self._headers)