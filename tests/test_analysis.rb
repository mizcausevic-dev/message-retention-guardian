require "minitest/autorun"
require_relative "../lib/message_retention_guardian/analysis"

class AnalysisTest < Minitest::Test
  def test_summary_counts
    summary = MessageRetentionGuardian::Analysis.summary
    assert_equal 5, summary[:active_policies]
    assert_equal 3, summary[:legal_holds]
    assert_equal 2, summary[:urgent_risks]
  end

  def test_high_pressure_request_freezes
    result = MessageRetentionGuardian::Analysis.evaluate(
      "pending_deletions" => 1882,
      "retention_gap_days" => 14,
      "export_backlog" => 6,
      "shadow_channels" => 4,
      "region_mismatch" => true
    )

    assert_equal "freeze", result[:status]
    assert_operator result[:risk_score], :>=, 28
  end
end

