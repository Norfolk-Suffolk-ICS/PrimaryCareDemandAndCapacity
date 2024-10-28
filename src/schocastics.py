from typing import Callable, Dict, Literal, Type, Any

from scipy.stats import lognorm, expon
import numpy as np

import constants as const
from pydantic import Field, BaseModel

APPOINTMENT_LOWER_LIMIT_MINUTES = 1
APPOINTMENT_UPPER_LIMIT_MINUTES = 60
NUM_SAMPLES = 1000000
AREAS = ['acute', 'community']
DIST_TYPES:Dict[str, Callable]= {'lognormal': lognorm, 'exponential': expon}

class AppointmentDistribution(BaseModel):
    dist_type: Literal['lognormal', 'exponential'] = 'lognormal'
    lower_limit:int = Field(default=APPOINTMENT_LOWER_LIMIT_MINUTES)
    upper_limit:int = Field(default=APPOINTMENT_UPPER_LIMIT_MINUTES)
    params:Dict[str, Any] = Field(..., default_factory=dict)

    def create_samples(self, n_samples=NUM_SAMPLES)->np.ndarray:
        """
        Create samples from the distribution and filter out samples that are outside the lower and upper limits
        """
        dist_samples = DIST_TYPES[self.dist_type].rvs(**self.params, size=n_samples)
            # filter distribution
        return dist_samples[(dist_samples >= self.lower_limit) & (dist_samples <= self.upper_limit)]

    def create_pdf(self, x:np.ndarray)->np.ndarray:
        """
        Create the probability density function for the distribution
        """
        return DIST_TYPES[self.dist_type].pdf(x=x, **self.params)