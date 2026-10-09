Alert Triage Assistant

A lightweight, explainable alert triage tool designed to assist Level 1 Security Operations Center (SOC) analysts in classifying security alerts and determining the appropriate next action.

Overview

Security alert triage requires analysts to distinguish genuine security threats from false positives and events that require further investigation. This project aims to support that process by combining rule-based logic with classical machine learning techniques to analyze alert characteristics and provide transparent, reason-based triage recommendations.

Given an alert as input, the tool produces one of three verdicts:

Notify — The alert warrants notification or escalation to the relevant party.
False Positive (FP) — The alert is assessed as non-threatening or not actionable based on the available evidence.
Needs Review — The alert requires further investigation, validation, or higher-level analyst review.

The goal is not to replace human analysts, but to provide a practical decision-support tool that improves triage consistency, makes reasoning more transparent, and reduces repetitive manual work.
