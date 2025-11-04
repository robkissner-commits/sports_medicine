import React from 'react';
import '../styles/RiskBreakdown.css';

const RiskBreakdown = ({ riskData }) => {
  if (!riskData) {
    return <div className="risk-breakdown">No risk data available</div>;
  }

  const getRiskColor = (level) => {
    if (!level) return '#999';
    switch (level.toLowerCase()) {
      case 'high':
        return '#dc3545';
      case 'medium':
        return '#ffc107';
      case 'low':
        return '#28a745';
      default:
        return '#999';
    }
  };

  const getModifierColor = (value) => {
    if (!value) return '#6c757d';
    if (value >= 1.4) return '#dc3545'; // Red
    if (value >= 1.2) return '#fd7e14'; // Orange
    if (value >= 1.1) return '#ffc107'; // Yellow
    return '#28a745'; // Green
  };

  const getModifierLabel = (value) => {
    if (!value || value === 1.0) return 'Normal';
    if (value >= 1.4) return 'Very High Risk';
    if (value >= 1.2) return 'High Risk';
    if (value >= 1.1) return 'Elevated Risk';
    return 'Normal';
  };

  const getMonotonyStatus = (value) => {
    if (!value) return { label: 'Unknown', color: '#999' };
    if (value > 2.0) return { label: 'High (Dangerous)', color: '#dc3545' };
    if (value > 1.5) return { label: 'Elevated', color: '#ffc107' };
    return { label: 'Normal', color: '#28a745' };
  };

  const getZScoreStatus = (value) => {
    if (!value) return { label: 'Normal', color: '#28a745' };
    if (value > 2.5) return { label: 'Extreme Spike', color: '#dc3545' };
    if (value > 2.0) return { label: 'Significant Spike', color: '#fd7e14' };
    if (value > 1.5) return { label: 'Moderate Spike', color: '#ffc107' };
    return { label: 'Normal', color: '#28a745' };
  };

  const monotonyStatus = getMonotonyStatus(riskData.training_monotony);
  const zScoreStatus = getZScoreStatus(riskData.max_z_score_7d);

  return (
    <div className="risk-breakdown">
      <h2>Enhanced Risk Assessment</h2>

      {/* Overall Risk Score */}
      <div className="risk-overview">
        <div className="risk-score-card" style={{ borderColor: getRiskColor(riskData.risk_level) }}>
          <h3>Overall Risk</h3>
          <div className="risk-score" style={{ color: getRiskColor(riskData.risk_level) }}>
            {riskData.overall_risk_score?.toFixed(1) || 'N/A'}
          </div>
          <div className="risk-level" style={{ color: getRiskColor(riskData.risk_level) }}>
            {(riskData.risk_level || 'Unknown').toUpperCase()}
          </div>
        </div>

        {riskData.compound_multiplier && riskData.compound_multiplier > 1.0 && (
          <div className="compound-alert">
            <h4>⚠️ Compound Risk Multiplier</h4>
            <div className="multiplier-value" style={{ color: getModifierColor(riskData.compound_multiplier) }}>
              {riskData.compound_multiplier.toFixed(2)}×
            </div>
            <p>Multiple risk factors are combining to increase injury risk</p>
          </div>
        )}
      </div>

      {/* Traditional Metrics */}
      <div className="metrics-section">
        <h3>Traditional Metrics</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-label">ACWR</div>
            <div className="metric-value">{riskData.acwr?.toFixed(2) || 'N/A'}</div>
            <div className="metric-subtext">
              {riskData.acwr > 1.5 ? '⚠️ Too High' : riskData.acwr < 0.8 ? '⚠️ Too Low' : '✓ Optimal'}
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Acute Load (7d)</div>
            <div className="metric-value">{riskData.acute_load?.toFixed(1) || 'N/A'}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Chronic Load (28d)</div>
            <div className="metric-value">{riskData.chronic_load?.toFixed(1) || 'N/A'}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Recovery Score</div>
            <div className="metric-value">{riskData.recovery_score?.toFixed(0) || 'N/A'}</div>
            <div className="metric-subtext">
              {riskData.recovery_score < 40 ? '⚠️ Low' : riskData.recovery_score < 60 ? '→ Moderate' : '✓ Good'}
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Lifestyle Score</div>
            <div className="metric-value">{riskData.lifestyle_score?.toFixed(0) || 'N/A'}</div>
            <div className="metric-subtext">
              {riskData.lifestyle_score < 50 ? '⚠️ Poor' : riskData.lifestyle_score < 70 ? '→ Fair' : '✓ Good'}
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Metrics (NEW) */}
      <div className="metrics-section enhanced">
        <h3>🆕 Enhanced Metrics (Research-Based)</h3>
        <div className="metrics-grid">
          <div className="metric-card highlight">
            <div className="metric-label">Training Monotony</div>
            <div className="metric-value" style={{ color: monotonyStatus.color }}>
              {riskData.training_monotony?.toFixed(2) || 'N/A'}
            </div>
            <div className="metric-subtext" style={{ color: monotonyStatus.color }}>
              {monotonyStatus.label}
            </div>
            <div className="metric-info">Foster et al., 1998</div>
          </div>

          <div className="metric-card highlight">
            <div className="metric-label">Training Strain</div>
            <div className="metric-value">
              {riskData.training_strain?.toFixed(0) || 'N/A'}
            </div>
            <div className="metric-subtext">
              {riskData.training_strain > 3000 ? '⚠️ Very High' : riskData.training_strain > 2000 ? '→ Elevated' : '✓ Normal'}
            </div>
            <div className="metric-info">Load × Monotony</div>
          </div>

          <div className="metric-card highlight">
            <div className="metric-label">Z-Score (Max 7d)</div>
            <div className="metric-value" style={{ color: zScoreStatus.color }}>
              {riskData.max_z_score_7d?.toFixed(2) || 'N/A'}
            </div>
            <div className="metric-subtext" style={{ color: zScoreStatus.color }}>
              {zScoreStatus.label}
            </div>
            <div className="metric-info">Spike Detection</div>
          </div>

          <div className="metric-card highlight">
            <div className="metric-label">Current Z-Score</div>
            <div className="metric-value">
              {riskData.current_z_score?.toFixed(2) || 'N/A'}
            </div>
            <div className="metric-subtext">vs Baseline</div>
          </div>
        </div>
      </div>

      {/* Risk Modifiers */}
      <div className="metrics-section modifiers">
        <h3>🔬 Risk Modifiers (Compound Scoring)</h3>
        <div className="modifiers-grid">
          <div className="modifier-card">
            <div className="modifier-icon">😴</div>
            <div className="modifier-label">Sleep</div>
            <div className="modifier-value" style={{ color: getModifierColor(riskData.sleep_modifier) }}>
              {riskData.sleep_modifier?.toFixed(2)}×
            </div>
            <div className="modifier-status" style={{ color: getModifierColor(riskData.sleep_modifier) }}>
              {getModifierLabel(riskData.sleep_modifier)}
            </div>
          </div>

          <div className="modifier-card">
            <div className="modifier-icon">🧠</div>
            <div className="modifier-label">Stress</div>
            <div className="modifier-value" style={{ color: getModifierColor(riskData.stress_modifier) }}>
              {riskData.stress_modifier?.toFixed(2)}×
            </div>
            <div className="modifier-status" style={{ color: getModifierColor(riskData.stress_modifier) }}>
              {getModifierLabel(riskData.stress_modifier)}
            </div>
          </div>

          <div className="modifier-card">
            <div className="modifier-icon">🏥</div>
            <div className="modifier-label">Injury Recency</div>
            <div className="modifier-value" style={{ color: getModifierColor(riskData.injury_recency_modifier) }}>
              {riskData.injury_recency_modifier?.toFixed(2)}×
            </div>
            <div className="modifier-status" style={{ color: getModifierColor(riskData.injury_recency_modifier) }}>
              {getModifierLabel(riskData.injury_recency_modifier)}
            </div>
          </div>

          <div className="modifier-card">
            <div className="modifier-icon">📅</div>
            <div className="modifier-label">Age</div>
            <div className="modifier-value" style={{ color: getModifierColor(riskData.age_modifier) }}>
              {riskData.age_modifier?.toFixed(2)}×
            </div>
            <div className="modifier-status" style={{ color: getModifierColor(riskData.age_modifier) }}>
              {getModifierLabel(riskData.age_modifier)}
            </div>
          </div>
        </div>

        <div className="modifier-explanation">
          <p>
            <strong>How it works:</strong> Risk modifiers multiply together to create compound risk.
            For example, poor sleep (1.4×) + recent injury (1.5×) = 2.1× total risk multiplier.
          </p>
        </div>
      </div>

      {/* Recommendations */}
      {riskData.recommendations && (
        <div className="recommendations-section">
          <h3>📋 Recommendations</h3>
          <div className="recommendations-content">
            {riskData.recommendations.split('\n\n').map((rec, index) => (
              <div key={index} className="recommendation-item">
                {rec}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskBreakdown;
