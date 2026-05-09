import pytest
from unittest.mock import AsyncMock, patch
from pipeline.classifier import DocumentClassifier
from pipeline.orchestrator import PipelineOrchestrator

def test_classifier_invoice():
    clf = DocumentClassifier()
    label, confidence = clf.classify("Invoice #1234 Amount Due: $5,000 Payment due in 30 days")
    assert label == "invoice"
    assert confidence > 0.75

def test_classifier_contract():
    clf = DocumentClassifier()
    label, confidence = clf.classify("This agreement between the parties clause 1 terms and conditions")
    assert label == "contract"

def test_classifier_confidence_range():
    clf = DocumentClassifier()
    _, confidence = clf.classify("some text")
    assert 0.0 <= confidence <= 1.0

@pytest.mark.asyncio
async def test_pipeline_orchestrator_status():
    orchestrator = PipelineOrchestrator()
    result = orchestrator.get_job_status("nonexistent-id")
    assert result["status"] == "not_found"
