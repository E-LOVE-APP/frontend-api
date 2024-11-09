from enum import Enum


class MatchingType(Enum):
    STANDARD = "standard"
    MAX_COMPATIBILITY = "max_compatibility"
    OPPOSITES_ATTRACT = "opposites_attract"


MATCHING_PERCENTAGE_RANGES = {
    MatchingType.STANDARD: (20, 40),
    MatchingType.MAX_COMPATIBILITY: (80, 100),
    MatchingType.OPPOSITES_ATTRACT: (10, 20),
}
