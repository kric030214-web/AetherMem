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
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class InteractionMetrics:
    """Interaction frequency and recency analysis."""

    def __init__(self, window_days: int = 30):
        """
        Initialize interaction metrics tracker.

        Args:
            window_days: Analysis window in days (default: 30)
        """
        self.window_days = window_days
        self.interactions: Dict[str, List[datetime]] = defaultdict(list)

    def record_interaction(self, entity_id: str, timestamp: Optional[datetime] = None) -> None:
        """
        Record an interaction.

        Args:
            entity_id: Entity identifier
            timestamp: Interaction timestamp (default: current time)
        """
        if timestamp is None:
            timestamp = datetime.now()

        self.interactions[entity_id].append(timestamp)

        # Clean up old interactions outside window
        self._cleanup_old_interactions(entity_id)

    def calculate_frequency(self, entity_id: str, window_days: Optional[int] = None) -> float:
        """
        Calculate interaction frequency.

        Args:
            entity_id: Entity identifier
            window_days: Optional custom window size

        Returns:
            Frequency score (0-1)
        """
        if entity_id not in self.interactions:
            return 0.0

        window = window_days or self.window_days
        cutoff = datetime.now() - timedelta(days=window)

        # Count interactions within window
        recent_interactions = [ts for ts in self.interactions[entity_id] if ts >= cutoff]

        if not recent_interactions:
            return 0.0

        # Normalize frequency: interactions per day
        avg_interactions_per_day = len(recent_interactions) / window

        # Sigmoid normalization to 0-1 range
        # Maximum expected: 10 interactions per day = frequency 0.95
        frequency = 1 / (1 + math.exp(-(avg_interactions_per_day - 2)))

        return max(0.0, min(1.0, frequency))

    def calculate_recency(self, entity_id: str) -> float:
        """
        Calculate interaction recency.

        Args:
            entity_id: Entity identifier

        Returns:
            Recency score (0-1, 1 = most recent)
        """
        if entity_id not in self.interactions or not self.interactions[entity_id]:
            return 0.0

        # Get most recent interaction
        latest_interaction = max(self.interactions[entity_id])
        now = datetime.now()

        # Calculate time difference in hours
        time_diff = now - latest_interaction
        hours_diff = time_diff.total_seconds() / 3600

        # Exponential decay: recency = e^(-λ * t)
        # Half-life of 24 hours for recency
        decay_rate = math.log(2) / 24  # λ = ln(2) / t½
        recency = math.exp(-decay_rate * hours_diff)

        return max(0.0, min(1.0, recency))

    def calculate_engagement(self, entity_id: str) -> float:
        """
        Calculate overall engagement score.

        Args:
            entity_id: Entity identifier

        Returns:
            Engagement score (0-1)
        """
        frequency = self.calculate_frequency(entity_id)
        recency = self.calculate_recency(entity_id)

        # Weighted combination
        engagement = (0.6 * frequency) + (0.4 * recency)

        return max(0.0, min(1.0, engagement))

    def detect_patterns(self, entity_id: str) -> Dict[str, Any]:
        """
        Detect interaction patterns.

        Args:
            entity_id: Entity identifier

        Returns:
            Pattern analysis dictionary
        """
        if entity_id not in self.interactions:
            return {"status": "no_interactions"}

        interactions = self.interactions[entity_id]
        if not interactions:
            return {"status": "no_interactions"}

        # Sort interactions
        sorted_interactions = sorted(interactions)

        # Calculate time differences
        time_diffs = []
        for i in range(1, len(sorted_interactions)):
            diff = (sorted_interactions[i] - sorted_interactions[i - 1]).total_seconds() / 3600
            time_diffs.append(diff)

        patterns = {
            "total_interactions": len(interactions),
            "first_interaction": sorted_interactions[0].isoformat(),
            "last_interaction": sorted_interactions[-1].isoformat(),
            "interaction_duration_days": (sorted_interactions[-1] - sorted_interactions[0]).total_seconds()
            / (24 * 3600),
        }

        if time_diffs:
            avg_diff = sum(time_diffs) / len(time_diffs)
            patterns.update(
                {
                    "avg_hours_between": avg_diff,
                    "min_hours_between": min(time_diffs),
                    "max_hours_between": max(time_diffs),
                    "std_hours_between": self._calculate_std(time_diffs, avg_diff),
                }
            )

            # Detect regularity
            if len(time_diffs) >= 3:
                regularity = 1 / (1 + patterns["std_hours_between"])
                patterns["regularity_score"] = max(0.0, min(1.0, regularity))

        return patterns

    def get_entity_stats(self, entity_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for an entity.

        Args:
            entity_id: Entity identifier

        Returns:
            Statistics dictionary
        """
        stats = {
            "entity_id": entity_id,
            "total_interactions": len(self.interactions.get(entity_id, [])),
            "frequency_score": self.calculate_frequency(entity_id),
            "recency_score": self.calculate_recency(entity_id),
            "engagement_score": self.calculate_engagement(entity_id),
        }

        # Add pattern analysis
        patterns = self.detect_patterns(entity_id)
        if patterns and "status" in patterns and patterns["status"] != "no_interactions":
            stats.update(patterns)
            del stats["status"]

        return stats

    def get_all_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all entities.

        Returns:
            Dictionary with all entity statistics
        """
        all_stats = {}

        for entity_id in self.interactions:
            all_stats[entity_id] = self.get_entity_stats(entity_id)

        summary = {
            "total_entities": len(self.interactions),
            "total_interactions": sum(len(interactions) for interactions in self.interactions.values()),
            "entities": all_stats,
        }

        return summary

    def _cleanup_old_interactions(self, entity_id: str) -> None:
        """
        Clean up interactions older than window.

        Args:
            entity_id: Entity identifier
        """
        cutoff = datetime.now() - timedelta(days=self.window_days)

        self.interactions[entity_id] = [ts for ts in self.interactions[entity_id] if ts >= cutoff]

        # Remove entity if no interactions remain
        if not self.interactions[entity_id]:
            del self.interactions[entity_id]

    def _calculate_std(self, values: List[float], mean: float) -> float:
        """
        Calculate standard deviation.

        Args:
            values: List of values
            mean: Mean of values

        Returns:
            Standard deviation
        """
        if len(values) <= 1:
            return 0.0

        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)


class TimeSeriesAnalyzer:
    """Time series analysis for interaction patterns."""

    def __init__(self, resolution_hours: int = 1):
        """
        Initialize time series analyzer.

        Args:
            resolution_hours: Time resolution in hours (default: 1)
        """
        self.resolution_hours = resolution_hours

    def create_time_series(self, interactions: List[datetime], window_days: int = 7) -> Dict[str, List[float]]:
        """
        Create time series from interactions.

        Args:
            interactions: List of interaction timestamps
            window_days: Analysis window in days

        Returns:
            Time series data
        """
        if not interactions:
            return {"timestamps": [], "counts": []}

        # Sort interactions
        sorted_interactions = sorted(interactions)

        # Determine time range
        start_time = sorted_interactions[0]
        end_time = sorted_interactions[-1]

        # Create time bins
        bin_size = timedelta(hours=self.resolution_hours)
        current_bin = start_time.replace(minute=0, second=0, microsecond=0)

        bins = []
        counts = []

        while current_bin <= end_time + bin_size:
            bin_end = current_bin + bin_size

            # Count interactions in this bin
            count = sum(1 for ts in sorted_interactions if current_bin <= ts < bin_end)

            bins.append(current_bin.isoformat())
            counts.append(count)

            current_bin += bin_size

        return {
            "timestamps": bins,
            "counts": counts,
            "resolution_hours": self.resolution_hours,
            "total_interactions": len(interactions),
        }

    def detect_periodicity(self, time_series: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Detect periodicity in time series.

        Args:
            time_series: Time series data

        Returns:
            Periodicity analysis
        """
        counts = time_series["counts"]

        if len(counts) < 24:  # Need at least 24 hours of data
            return {"detected": False, "reason": "insufficient_data"}

        # Simple autocorrelation for daily patterns
        max_lag = min(168, len(counts) // 2)  # Up to 1 week

        autocorrelations = []
        for lag in range(1, max_lag + 1):
            if lag >= len(counts):
                break

            # Calculate autocorrelation at this lag
            corr = self._calculate_autocorrelation(counts, lag)
            autocorrelations.append((lag, corr))

        # Find peaks in autocorrelation
        peaks = self._find_peaks(autocorrelations, threshold=0.3)

        analysis = {
            "detected": len(peaks) > 0,
            "autocorrelation_peaks": peaks,
            "max_correlation": max(corr for _, corr in autocorrelations) if autocorrelations else 0.0,
        }

        if peaks:
            # Most likely period (in hours)
            likely_period = peaks[0][0] * self.resolution_hours
            analysis["likely_period_hours"] = likely_period

            if 20 <= likely_period <= 28:  # Daily pattern
                analysis["pattern"] = "daily"
            elif likely_period <= 12:  # Multiple times per day
                analysis["pattern"] = "multiple_daily"
            elif likely_period >= 160:  # Weekly pattern
                analysis["pattern"] = "weekly"

        return analysis

    def _calculate_autocorrelation(self, series: List[float], lag: int) -> float:
        """
        Calculate autocorrelation at given lag.

        Args:
            series: Time series data
            lag: Lag value

        Returns:
            Autocorrelation coefficient
        """
        n = len(series)
        if n <= lag:
            return 0.0

        mean = sum(series) / n
        variance = sum((x - mean) ** 2 for x in series) / n

        if variance == 0:
            return 0.0

        # Calculate autocorrelation
        numerator = sum((series[i] - mean) * (series[i + lag] - mean) for i in range(n - lag))

        autocorr = numerator / (variance * (n - lag))
        return autocorr

    def _find_peaks(self, correlations: List[tuple], threshold: float = 0.3) -> List[tuple]:
        """
        Find peaks in correlation sequence.

        Args:
            correlations: List of (lag, correlation) tuples
            threshold: Minimum correlation threshold

        Returns:
            List of peak (lag, correlation) tuples
        """
        peaks = []

        for i in range(1, len(correlations) - 1):
            prev_lag, prev_corr = correlations[i - 1]
            curr_lag, curr_corr = correlations[i]
            next_lag, next_corr = correlations[i + 1]

            if curr_corr > threshold and curr_corr > prev_corr and curr_corr > next_corr:
                peaks.append((curr_lag, curr_corr))

        # Sort by correlation (descending)
        peaks.sort(key=lambda x: x[1], reverse=True)

        return peaks


def create_default_metrics() -> InteractionMetrics:
    """
    Create default interaction metrics tracker.

    Returns:
        InteractionMetrics instance
    """
    return InteractionMetrics(window_days=30)


def create_time_series_analyzer() -> TimeSeriesAnalyzer:
    """
    Create time series analyzer.

    Returns:
        TimeSeriesAnalyzer instance
    """
    return TimeSeriesAnalyzer(resolution_hours=1)
