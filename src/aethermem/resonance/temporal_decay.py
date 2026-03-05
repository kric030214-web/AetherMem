"""
AetherMem - Memory Continuity Protocol for AI Agents
Copyright (C) 2026 kric030214-web

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class TemporalDecay:
    """Temporal decay calculations for memory weighting."""

    def __init__(self, decay_rate: float = 0.1):
        """
        Initialize temporal decay calculator.

        Args:
            decay_rate: Decay rate per day (default: 0.1 = 10% per day)
        """
        self.decay_rate = decay_rate

    def calculate_decay_weight(self, timestamp: datetime, reference_time: Optional[datetime] = None) -> float:
        """
        Calculate decay weight based on time difference.

        Args:
            timestamp: Timestamp of the memory
            reference_time: Reference time (default: current time)

        Returns:
            Decay weight between 0 and 1
        """
        if reference_time is None:
            reference_time = datetime.now()

        # Calculate time difference in days
        time_diff = reference_time - timestamp
        days_diff = time_diff.total_seconds() / (24 * 3600)

        # Exponential decay: weight = e^(-λ * t)
        weight = math.exp(-self.decay_rate * days_diff)

        # Ensure weight is between 0 and 1
        return max(0.0, min(1.0, weight))

    def calculate_half_life(self) -> float:
        """
        Calculate half-life in days.

        Returns:
            Half-life in days
        """
        # Half-life formula: t½ = ln(2) / λ
        if self.decay_rate <= 0:
            return float("inf")

        half_life = math.log(2) / self.decay_rate
        return half_life

    def calculate_effective_weight(
        self, timestamp: datetime, base_weight: float = 1.0, reference_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate effective weight with temporal decay.

        Args:
            timestamp: Timestamp of the memory
            base_weight: Base weight before decay
            reference_time: Reference time

        Returns:
            Effective weight after decay
        """
        decay_weight = self.calculate_decay_weight(timestamp, reference_time)
        effective_weight = base_weight * decay_weight

        return effective_weight

    def get_decay_stats(self) -> Dict[str, Any]:
        """
        Get decay statistics.

        Returns:
            Dictionary with decay statistics
        """
        half_life = self.calculate_half_life()

        stats = {
            "decay_rate": self.decay_rate,
            "half_life_days": half_life,
            "decay_per_week": 1 - math.exp(-self.decay_rate * 7),
            "decay_per_month": 1 - math.exp(-self.decay_rate * 30),
            "retention_1_day": math.exp(-self.decay_rate),
            "retention_7_days": math.exp(-self.decay_rate * 7),
            "retention_30_days": math.exp(-self.decay_rate * 30),
        }

        return stats


class AdaptiveDecay(TemporalDecay):
    """Adaptive temporal decay with variable rates."""

    def __init__(self, base_decay_rate: float = 0.1, importance_factor: float = 0.5, frequency_factor: float = 0.3):
        """
        Initialize adaptive decay calculator.

        Args:
            base_decay_rate: Base decay rate per day
            importance_factor: Importance impact on decay rate (0-1)
            frequency_factor: Frequency impact on decay rate (0-1)
        """
        super().__init__(base_decay_rate)
        self.importance_factor = importance_factor
        self.frequency_factor = frequency_factor

    def calculate_adaptive_decay_rate(self, importance: float, frequency: float) -> float:
        """
        Calculate adaptive decay rate based on importance and frequency.

        Args:
            importance: Importance score (0-1)
            frequency: Interaction frequency (0-1)

        Returns:
            Adaptive decay rate
        """
        # Higher importance = slower decay
        importance_effect = 1 - (importance * self.importance_factor)

        # Higher frequency = slower decay
        frequency_effect = 1 - (frequency * self.frequency_factor)

        # Combine effects
        adaptive_rate = self.decay_rate * importance_effect * frequency_effect

        # Ensure minimum decay rate
        min_rate = self.decay_rate * 0.1
        return max(min_rate, adaptive_rate)

    def calculate_adaptive_weight(
        self,
        timestamp: datetime,
        importance: float = 0.5,
        frequency: float = 0.5,
        reference_time: Optional[datetime] = None,
    ) -> float:
        """
        Calculate adaptive weight with importance and frequency.

        Args:
            timestamp: Timestamp of the memory
            importance: Importance score (0-1)
            frequency: Interaction frequency (0-1)
            reference_time: Reference time

        Returns:
            Adaptive weight
        """
        # Calculate adaptive decay rate
        adaptive_rate = self.calculate_adaptive_decay_rate(importance, frequency)

        # Calculate time difference
        if reference_time is None:
            reference_time = datetime.now()

        time_diff = reference_time - timestamp
        days_diff = time_diff.total_seconds() / (24 * 3600)

        # Calculate weight with adaptive decay
        weight = math.exp(-adaptive_rate * days_diff)

        # Apply importance boost
        importance_boost = 1 + (importance * 0.5)  # Up to 50% boost

        final_weight = weight * importance_boost

        return max(0.0, min(1.0, final_weight))


def create_default_decay() -> TemporalDecay:
    """
    Create default temporal decay calculator.

    Returns:
        TemporalDecay instance
    """
    return TemporalDecay(decay_rate=0.1)


def create_adaptive_decay() -> AdaptiveDecay:
    """
    Create adaptive temporal decay calculator.

    Returns:
        AdaptiveDecay instance
    """
    return AdaptiveDecay(base_decay_rate=0.1, importance_factor=0.5, frequency_factor=0.3)
