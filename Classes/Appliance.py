# Definition of Appliance classe


class Appliance:
    def __init__(self):
        # Attributs :
        self.disutility = 0.1   # Prefered Delay
        self.p = 0.0    # Power consumption
        list_r = []     # Reservation time
        t = 0   # Duration time of an appliance
        list_US = []  # Start time of uinterruptible appliance (Not use)
        list_S = []  # Operation Time
        tau = 0  # end time of appliance
