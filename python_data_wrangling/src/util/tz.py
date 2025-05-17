from pytz import timezone
import pytz

# This class is used for Timezone logic.
# Chris Joakim, 2025


class Tz:
    @classmethod
    def common_timezone_list(cls):
        """Return the list of common timezone names."""
        return pytz.common_timezones

    @classmethod
    def all_timezones(cls):
        """Return all the defined pytz timezones."""
        return pytz.all_timezones

    @classmethod
    def gmt_tz(cls):
        """Return the pytz GMT timezone object."""
        return timezone("GMT")

    @classmethod
    def paris_tz(cls):
        """Return the pytz Paris timezone object."""
        return timezone("Europe/Paris")

    @classmethod
    def tokyo_tz(cls):
        """Return the pytz Tokyo timezone object."""
        return timezone("Asia/Tokyo")

    @classmethod
    def uk_tz(cls):
        """Return the pytz UK timezone object."""
        return timezone("Europe/London")

    @classmethod
    def eastus_tz(cls):
        """Return the pytz East US timezone object."""
        return timezone("America/New_York")

    @classmethod
    def westus_tz(cls):
        """Return the pytz West US timezone object."""
        return timezone("America/Los_Angeles")
