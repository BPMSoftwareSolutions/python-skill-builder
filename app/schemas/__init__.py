"""
Workshop Schema Module
Defines data structures for TDD-first workshop learning platform
"""

from .workshop import Workshop, WorkshopPhase, WorkshopPhases
from .test_suite import TestCase, TestSuite, AssertionType
from .mock_data import MockDataPoint, MockDataSet
from .phase_guidance import PhaseGuidance, RedPhaseGuidance, GreenPhaseGuidance, RefactorPhaseGuidance

__all__ = [
    'Workshop',
    'WorkshopPhase',
    'WorkshopPhases',
    'TestCase',
    'TestSuite',
    'AssertionType',
    'MockDataPoint',
    'MockDataSet',
    'PhaseGuidance',
    'RedPhaseGuidance',
    'GreenPhaseGuidance',
    'RefactorPhaseGuidance',
]

