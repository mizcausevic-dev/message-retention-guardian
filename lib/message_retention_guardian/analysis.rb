require_relative "sample_data"

module MessageRetentionGuardian
  class Analysis
    def self.summary
      SAMPLE_DATA[:dashboard]
    end

    def self.sample_request
      SAMPLE_DATA[:requests].first
    end

    def self.policies
      SAMPLE_DATA[:policies]
    end

    def self.requests
      SAMPLE_DATA[:requests]
    end

    def self.find_request(request_id)
      SAMPLE_DATA[:requests].find { |item| item[:id] == request_id }
    end

    def self.evaluate(payload)
      pending_deletions = payload.fetch("pending_deletions", 0).to_i
      gap = payload.fetch("retention_gap_days", 0).to_i
      backlog = payload.fetch("export_backlog", 0).to_i
      shadow = payload.fetch("shadow_channels", 0).to_i
      mismatch = payload.fetch("region_mismatch", false)

      score = (pending_deletions / 250.0) + (gap * 1.6) + (backlog * 3.0) + (shadow * 2.5)
      score += 8 if mismatch

      status =
        if score >= 28
          "freeze"
        elsif score >= 14
          "watch"
        else
          "clear"
        end

      next_action =
        case status
        when "freeze"
          "Pause deletion jobs, lock the legal hold scope, and export the at-risk lane before any scheduler catches up."
        when "watch"
          "Tighten the hold filter, verify regional residency, and clear backlog before the next deletion window."
        else
          "Retention lane is stable. Keep the schedule and audit the next run."
        end

      {
        status: status,
        risk_score: score.round(1),
        next_action: next_action,
        factors: {
          retention_gap_days: gap,
          pending_deletions: pending_deletions,
          export_backlog: backlog,
          shadow_channels: shadow,
          region_mismatch: mismatch
        }
      }
    end
  end
end
