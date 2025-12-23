


class Global:
    shark_time=0
    Ice_death_count=0



    @classmethod
    def add_ice_death(cls,count):
        cls.Ice_death_count+=count

    @classmethod
    def read_ice_death(cls):
        a=cls.Ice_death_count
        cls.Ice_death_count=0
        return a

