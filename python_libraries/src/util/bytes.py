from numbers import Number

# This class is used to calculate KB, MB, GB, TB, PB, and EB values
# from a given number of bytes.  It also provides as_xxx() translation
# methods.
# Chris Joakim, 2025


class Bytes:
    @classmethod
    def kilobyte(cls) -> int:
        """Return the number of bytes in a kilobyte."""
        return 1024

    @classmethod
    def kilobytes(cls, kilobytes: Number) -> Number:
        """Return the number of bytes in the given KB value."""
        return Bytes.kilobyte() * abs(float(kilobytes))

    @classmethod
    def megabyte(cls) -> int:
        """Return the number of bytes in a megabyte."""
        return pow(1024, 2)

    @classmethod
    def megabytes(cls, megabytes: Number) -> Number:
        """Return the number of bytes in the given MB value."""
        return Bytes.megabyte() * abs(float(megabytes))

    @classmethod
    def gigabyte(cls) -> int:
        """Return the number of bytes in a gigabyte."""
        return pow(1024, 3)

    @classmethod
    def gigabytes(cls, gigabytes: Number) -> Number:
        """Return the number of bytes in the given GB value."""
        return Bytes.gigabyte() * abs(float(gigabytes))

    @classmethod
    def terabyte(cls) -> int:
        """Return the number of bytes in a terabyte."""
        return pow(1024, 4)

    @classmethod
    def terabytes(cls, terabytes: Number) -> Number:
        """Return the number of bytes in the given TB value."""
        return Bytes.terabyte() * abs(float(terabytes))

    @classmethod
    def petabyte(cls) -> int:
        """Return the number of bytes in a petabyte."""
        return pow(1024, 5)

    @classmethod
    def petabytes(cls, petabytes: Number) -> Number:
        """Return the number of bytes in the given PB value."""
        return Bytes.petabyte() * abs(float(petabytes))

    @classmethod
    def exabyte(cls) -> int:
        """Return the number of bytes in an exabyte."""
        return pow(1024, 6)

    @classmethod
    def exabytes(cls, exabytes: Number) -> Number:
        """Return the number of bytes in the given EB value."""
        return Bytes.exabyte() * abs(float(exabytes))

    @classmethod
    def as_kilobytes(cls, num_bytes: Number) -> Number:
        """Return the number of KB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.kilobyte())

    @classmethod
    def as_megabytes(cls, num_bytes: Number) -> Number:
        """Return the number of MB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.megabyte())

    @classmethod
    def as_gigabytes(cls, num_bytes: Number) -> Number:
        """Return the number of GB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.gigabyte())

    @classmethod
    def as_terabytes(cls, num_bytes: Number) -> Number:
        """Return the number of TB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.terabyte())

    @classmethod
    def as_petabytes(cls, num_bytes: Number) -> Number:
        """Return the number of PB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.petabyte())

    @classmethod
    def as_exabytes(cls, num_bytes: Number) -> Number:
        """Return the number of EB for the given number of bytes."""
        return float(abs(num_bytes)) / float(cls.exabyte())
